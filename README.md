# Coupon Information Extractor

This project is a Flask web application that extracts information from digital coupons using the Google Vision API. It allows users to upload an image of a coupon, and the application will extract relevant information such as the barcode, due date, items, price, and brand.

[<img width="411" alt="flask_application" src="https://github.com/llnOrmll/OCR_Digital_Coupons/assets/32804828/9993ce74-4898-4fdf-b6ea-edbfaae5b68e">](https://github.com/llnOrmll/OCR_Digital_Coupons/blob/main/sample_images/flask_application.png)

![result_sample](https://github.com/llnOrmll/OCR_Digital_Coupons/assets/32804828/6d3a63d0-0623-4570-8a28-3c07f9a97029)


## Features

- Utilizes Google Vision API for text detection and extraction
- Extracts barcode, due date, items, price, and brand from the coupon image
- Cleans and processes the extracted text using regular expressions and text cleaning techniques
- Matches the extracted information with a reference dataset stored in Google BigQuery
- Displays the extracted information on a results page
- Handles errors and provides informative error messages

## Prerequisites

Before running the application, ensure that you have the following:

- Python 3.x installed
- Google Cloud SDK installed and configured
- Google Cloud Storage bucket created
- Google BigQuery dataset and table set up with the reference data
- Google Cloud Vision API credentials file (`google_project_service_account_credentials.json`) placed in the project directory

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/coupon-information-extractor.git
   ```

2. Change into the project directory:
   ```
   cd coupon-information-extractor
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your Google Cloud Vision API credentials file:
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="google_project_service_account_credentials.json"
   ```

5. Update the `CLOUD_STORAGE_BUCKET` variable in the code with your Google Cloud Storage bucket name.

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Access the application in your web browser at `http://localhost:8888`.

3. Upload an image of a coupon using the provided form.

4. The application will process the image, extract the relevant information, and display the results on the next page.

## Technologies Used

- Python
- Flask
- Google Cloud Storage
- Google Cloud Vision API
- Google BigQuery
- scikit-learn (TfidfVectorizer, linear_kernel)
- Regular Expressions
- HTML/CSS

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
