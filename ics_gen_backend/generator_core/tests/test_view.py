from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("generator_core:upload")
        
    def test_valid_double_input(self):
        # Test Valid Input with Text and Image
        with open('generator_core/tests/sample_images/valid_image.png', 'rb') as file:
            uploaded_file = SimpleUploadedFile('valid_image.png', file.read(), content_type='image/png')
            data = {'text': 'a' * 500, 'image': uploaded_file}
            response = self.client.post(self.url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {"Message":"Valid Input"})
            
    def test_valid_text_only_input(self):
        # Test Valid Input with Text Only
        data = {'text': 'a' * 500}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"Message":"Valid Input"})
        
    def test_valid_image_only_input(self):
        # Test Valid Input with Image Only
        with open('generator_core/tests/sample_images/valid_image.png', 'rb') as file:
            uploaded_file = SimpleUploadedFile('valid_image.png', file.read(), content_type='image/png')
            data = {'image': uploaded_file}
            response = self.client.post(self.url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {"Message":"Valid Input"})
            
    def test_invalid_request_format(self):
        # Test Invalid Request Format
        data = {'text': 'a' * 500}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(response.data, {"Message":"Unsupported Media Type"})