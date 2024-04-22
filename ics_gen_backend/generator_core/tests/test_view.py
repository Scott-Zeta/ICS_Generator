from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("generator_core:upload")
        
    def test_valid_double_input(self):
        # Test Three Valid Input Cases
        text = "a" * 500
        test_cases = [
            {'text': text, 'file': 'valid_image.png'},
            {'text': text},
            {'file': 'valid_image.png'}
        ]

        for case in test_cases:
            data = {}
            if 'text' in case:
                data['text'] = case['text']
            if 'file' in case:
                # Have to open file multiple time because of the file pointer in file stream
                with open(f'generator_core/tests/sample_images/{case["file"]}', 'rb') as file:
                    uploaded_file = SimpleUploadedFile(case["file"], file.read(), content_type='image/png')
                    data['image'] = uploaded_file
            
            response = self.client.post(self.url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {"Message": "Valid Input"})
            
    def test_invalid_input(self):
        valid_text = "a" * 500
        invalid_text = "a" * 501
        test_cases = [
            {'text': invalid_text, 'file': 'valid_image.png'},
            {'text': valid_text, 'file': 'large_image.png'},
            {'text': valid_text, 'file': 'unsupported_format.svg'},
            {'text': valid_text, 'file': 'not_image.txt'},
            {}
        ]
        
        for case in test_cases:
            data = {}
            if 'text' in case:
                data['text'] = case['text']
            if 'file' in case:
                # Have to open file multiple time because of the file pointer in file stream
                with open(f'generator_core/tests/sample_images/{case["file"]}', 'rb') as file:
                    uploaded_file = SimpleUploadedFile(case["file"], file.read(), content_type='image/png')
                    data['image'] = uploaded_file

            response = self.client.post(self.url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
    def test_invalid_request_format(self):
        # Test Invalid Request Format
        data = {'text': 'a' * 500}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(response.data, {"Message":"Unsupported Media Type"})