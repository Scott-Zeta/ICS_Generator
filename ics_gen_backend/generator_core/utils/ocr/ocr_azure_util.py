import os
from dotenv import load_dotenv
import requests

class OCR_Azure_Exception(Exception):
    """Exception for errors encountered with Azure OCR service."""
    pass

def ocr_azure(validated_image):
    # validated_image should be an image in binary data that has passed validation
    
    # Set up Azure OCR API and request headers
    load_dotenv()
    endpoint = os.getenv('AZURE_OCR_ENDPOINT')
    subscription_key = os.getenv('AZURE_OCR_KEY')
    api_config = os.getenv('OCR_API_CONFIG')
    
    if not all([endpoint, subscription_key, api_config]):
        raise OCR_Azure_Exception("Missing required Azure OCR configuration.")

    text_recognition_url = endpoint + api_config
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}
    # image_data = open(validated_image, 'rb').read()

    # Send the request, parse the response and extract the text if successful
    try:
        response = requests.post(
            text_recognition_url, headers = headers, data = validated_image)
        
        # If not success code, goes into except block
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
            return " ".join(plaintext)
        else:
            return ""
    except requests.exceptions.HTTPError:
        status_code = response.status_code
        error_message = response.json().get('error', {}).get('message', 'Unknown Azure service error')
        raise OCR_Azure_Exception(f"HTTP Error {status_code}: {error_message}")
    except Exception as e:
        raise OCR_Azure_Exception(f"Internal Error: {str(e)}")

            
