import base64
import os
from flask import Flask, request, render_template
from google.cloud import storage
from google.cloud import vision
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
from google.cloud import bigquery
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./google_project_service_account_credentials.json"

app = Flask(__name__)

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = "project-gs-bucket-name"

@app.route('/')
def index() -> str:
    return """
<form method="POST" action="/upload" enctype="multipart/form-data">
    <input type="file" name="file">
    <input type="submit">
</form>
"""

def text_cleaning(string):
    s1 = re.sub(r'[]["()&,]', " ", string).strip()
    s2 = s1.replace(' +', '').replace('+', ' ')
    return ' '.join(s2.split())

@app.route('/upload', methods=['POST'])
def upload() -> str:
    """Process the uploaded file and upload it to Google Cloud Storage."""
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return 'No file uploaded.', 400

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )

    # Make the blob public. This is not necessary if the
    # entire bucket is public.
    # See https://cloud.google.com/storage/docs/access-control/making-data-public.
    #blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.

    content = blob.download_as_bytes()
    image = base64.b64encode(content).decode("utf-8")

    # vision client
    vision_client = vision.ImageAnnotatorClient()
    file_name = blob.public_url.split('/')[-1]
    img = vision.Image(source=vision.ImageSource(gcs_image_uri=f"gs://{CLOUD_STORAGE_BUCKET}/{file_name}"))
    text_detection_response = vision_client.text_detection(image=img)
    string = ' '.join([text.description for text in text_detection_response.text_annotations])
    string_cleaned = ' '.join(string.split('\n'))

    string_cleaned_nospace = ''.join(string_cleaned.split())
    try:
        barcode = re.search(r"\d{12}", string_cleaned_nospace)[0]
        duedate = re.search(r"\d{4}년\d{2}월\d{2}일", string_cleaned_nospace)[0]

        bqr = bigquery.Client()
        query = """
            SELECT * FROM `your_table_id`
        """
        references = bqr.query(query).to_dataframe()

        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(references['final'])

        first_barcode = barcode[:4]
        string_to_read = string_cleaned.split(first_barcode)[0].rstrip()
        string_final = text_cleaning(string_to_read)

        new_data = tfidf.transform([string_final])
        cosine_sim = linear_kernel(tfidf_matrix, new_data)
        idx = np.argmax(cosine_sim)

        items = references.iloc[idx]['items']
        price = references.iloc[idx]['price']
        brand = references.iloc[idx]['brand']

        return render_template('index.html', content=blob.content_type, image=image,
                               barcode=barcode, duedate=duedate, items=items, price=price, brand=brand)

    except TypeError:
        error_msg = "카카오 기프티콘을 올려주세요."
        return render_template('error.html', error_msg=error_msg)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8888, debug=True)

