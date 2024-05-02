import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Set the subscription key and endpoint for the OCR service
endpoint = os.getenv('AZURE_OCR_ENDPOINT')
subscription_key = os.getenv('AZURE_OCR_KEY')
api_config = os.getenv('OCR_API_CONFIG')
text_recognition_url = endpoint + api_config

# Set image_url to the URL of an image that you want to recognize.
image_path = "../../tests/sample_images/handwriting_printed_mixed_photo.jpeg"
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
image_data = open(image_path, 'rb').read()
response = requests.post(
    text_recognition_url, headers=headers, data=image_data)
response.raise_for_status()

analysis = response.json()

if 'readResult' in analysis:
    # Extract the text from the OCR result
    read_result_blocks = analysis['readResult']['blocks']
    plaintext = []
    for block in read_result_blocks:
        if 'lines' in block:
            for line in block['lines']:
                plaintext.append(line['text'])
    print(" ".join(plaintext))
else:
    print("No readResult")
    
    
