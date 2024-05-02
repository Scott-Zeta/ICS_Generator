import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Set the subscription key and endpoint for the OCR service
endpoint = os.getenv('AZURE_OCR_ENDPOINT')
subscription_key = os.getenv('AZURE_OCR_KEY')
text_recognition_url = endpoint + "/computervision/imageanalysis:analyze?api-version=2024-02-01&features=read&model-version=latest"

# Set image_url to the URL of an image that you want to recognize.
image_path = "../tests/sample_images/image_67161601.jpeg"
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
image_data = open(image_path, 'rb').read()
response = requests.post(
    text_recognition_url, headers=headers, data=image_data)
response.raise_for_status()

analysis = response.json()
print(analysis)