from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("generator_core:upload")
        
    def test_valid_input(self):
        with open('generator_core/tests/sample_images/valid_image.png', 'rb') as file:
            uploaded_file = SimpleUploadedFile('valid_image.png', file.read(), content_type='image/png')
            data = {'text': 'a' * 500, 'image': uploaded_file}
            response = self.client.post(self.url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {"Message":"Valid Input"})