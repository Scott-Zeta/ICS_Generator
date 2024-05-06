from django.test import TestCase
import requests
import requests_mock
from dotenv import load_dotenv
import os
from generator_core.utils.ocr.ocr_azure_util import ocr_azure, OCR_Azure_Exception

class TestOCR_Azure(TestCase):
    def setUp(self):
        # Set mock environment variables
        load_dotenv()
        self.endpoint = os.getenv('AZURE_OCR_ENDPOINT')
        self.api_config = os.getenv('OCR_API_CONFIG')
        self.subscription_key = 'fake_key'
        self.valid_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'  # Mock binary data of a valid image
    
    # @requests_mock.Mocker() is a decorator that simulate the mock request and response
    @requests_mock.Mocker()
    def test_ocr_azure_success(self, m):
        # Mock the API response for successful text extraction
        url = self.endpoint + self.api_config
        # Json from Azure documentation example response
        m.post(url, json={
            "modelVersion": "2024-02-01",
            "metadata":
            {
                "width": 1000,
                "height": 945
            },
            "readResult":
            {
                "blocks":
                [
                    {
                        "lines":
                        [
                            {
                                "text": "You must be the change you",
                                "boundingPolygon":
                                [
                                    {"x":251,"y":265},
                                    {"x":673,"y":260},
                                    {"x":674,"y":308},
                                    {"x":252,"y":318}
                                ],
                                "words":
                                [
                                    {"text":"You","boundingPolygon":[{"x":252,"y":267},{"x":307,"y":265},{"x":307,"y":318},{"x":253,"y":318}],"confidence":0.996},
                                    {"text":"must","boundingPolygon":[{"x":318,"y":264},{"x":386,"y":263},{"x":387,"y":316},{"x":319,"y":318}],"confidence":0.99},
                                    {"text":"be","boundingPolygon":[{"x":396,"y":262},{"x":432,"y":262},{"x":432,"y":315},{"x":396,"y":316}],"confidence":0.891},
                                    {"text":"the","boundingPolygon":[{"x":441,"y":262},{"x":503,"y":261},{"x":503,"y":312},{"x":442,"y":314}],"confidence":0.994},
                                    {"text":"change","boundingPolygon":[{"x":513,"y":261},{"x":613,"y":262},{"x":613,"y":306},{"x":513,"y":311}],"confidence":0.99},
                                    {"text":"you","boundingPolygon":[{"x":623,"y":262},{"x":673,"y":263},{"x":673,"y":302},{"x":622,"y":305}],"confidence":0.994}
                                ]
                            },
                            {
                                "text": "wish to see in the world !",
                                "boundingPolygon":
                                [
                                    {"x":325,"y":338},
                                    {"x":695,"y":328},
                                    {"x":696,"y":370},
                                    {"x":325,"y":381}
                                ],
                                "words":
                                [
                                    {"text":"wish","boundingPolygon":[{"x":325,"y":339},{"x":390,"y":337},{"x":391,"y":380},{"x":326,"y":381}],"confidence":0.992},
                                    {"text":"to","boundingPolygon":[{"x":406,"y":337},{"x":443,"y":335},{"x":443,"y":379},{"x":407,"y":380}],"confidence":0.995},
                                    {"text":"see","boundingPolygon":[{"x":451,"y":335},{"x":494,"y":334},{"x":494,"y":377},{"x":452,"y":379}],"confidence":0.996},
                                    {"text":"in","boundingPolygon":[{"x":502,"y":333},{"x":533,"y":332},{"x":534,"y":376},{"x":503,"y":377}],"confidence":0.996},
                                    {"text":"the","boundingPolygon":[{"x":542,"y":332},{"x":590,"y":331},{"x":590,"y":375},{"x":542,"y":376}],"confidence":0.995},
                                    {"text":"world","boundingPolygon":[{"x":599,"y":331},{"x":664,"y":329},{"x":664,"y":372},{"x":599,"y":374}],"confidence":0.995},
                                    {"text":"!","boundingPolygon":[{"x":672,"y":329},{"x":694,"y":328},{"x":694,"y":371},{"x":672,"y":372}],"confidence":0.957}
                                ]
                            }
                        ]
                    }
                ]
            }
        }, status_code=200)

        result = ocr_azure(self.valid_image)
        self.assertEqual(result, "You must be the change you wish to see in the world !")
    
    @requests_mock.Mocker()
    def test_ocr_azure_service_error(self, m):
        # Simulate the API response for service error
        url = self.endpoint + self.api_config
        code = "401"
        message = "Access denied due to invalid subscription key or wrong API endpoint. Make sure to provide a valid key for an active subscription and use a correct regional API endpoint for your resource."
        m.post(url, json={
            "error": {
                "code": code,
                "message": message
            }
            }, status_code=401)

        with self.assertRaises(OCR_Azure_Exception) as context:
            ocr_azure(self.valid_image)
        self.assertIn(f'HTTP Error {code}: {message}', str(context.exception))
        
    @requests_mock.Mocker()
    def test_ocr_azure_network_error(self, m):
        # Simulate a network error
        url = self.endpoint + self.api_config
        m.post(url, exc=requests.exceptions.ConnectTimeout)

        with self.assertRaises(OCR_Azure_Exception) as context:
            ocr_azure(self.valid_image)
        
        self.assertIn('Internal Error', str(context.exception))