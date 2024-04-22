from django.test import TestCase
from ..serializers import PostSerializer
from django.core.files.uploadedfile import SimpleUploadedFile

class UpLoad_Post_SerializerTestCase(TestCase):
    def test_validation_error_when_both_fields_empty(self):
        # Testing Empty Data
        serializer = PostSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Both text and image cannot be empty", serializer.errors['non_field_errors'])

    def test_validation_error_for_large_image(self):
        # Testing Large Image
        with open('generator_core/tests/sample_images/large_image.png', 'rb') as file:
            uploaded_file = SimpleUploadedFile('large_image.png', file.read(), content_type='image/png')
            data = {'image': uploaded_file}
            serializer = PostSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("File can not larger than 1MB", serializer.errors['image'])
    
    def test_validation_error_for_unsupported_image_format(self):
        # Testing Unsupported Image Format
        with open('generator_core/tests/sample_images/unsupported_format.svg', 'rb') as file:
            uploaded_file = SimpleUploadedFile('unsupported_format.svg', file.read(), content_type='image/svg')
            data = {'image': uploaded_file}
            serializer = PostSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("Upload a valid image. The file you uploaded was either not an image or a corrupted image.", serializer.errors['image'])
            
    def test_validation_error_for_non_image_file(self):
        # Testing Non-Image File
        with open('generator_core/tests/sample_images/not_image.txt', 'rb') as file:
            uploaded_file = SimpleUploadedFile('not_image.txt', file.read(), content_type='text/plain')
            data = {'image': uploaded_file}
            serializer = PostSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn("Upload a valid image. The file you uploaded was either not an image or a corrupted image.", serializer.errors['image'])

    def test_validation_error_for_extended_text(self):
        # Testing Extended Text
        long_text = "a" * 501
        data = {'text': long_text}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Ensure this field has no more than 500 characters.", serializer.errors['text'])
        
    def test_valid_data(self):
        # Testing Valid Input
        with open('generator_core/tests/sample_images/valid_image.png', 'rb') as file:
            uploaded_file = SimpleUploadedFile('valid_image.png', file.read(), content_type='image/png')
            valid_text = "a" * 500
            data = {'text': valid_text, 'image': uploaded_file}
            serializer = PostSerializer(data=data)
            self.assertTrue(serializer.is_valid())