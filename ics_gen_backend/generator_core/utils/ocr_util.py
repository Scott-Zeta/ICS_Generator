from PIL import Image
import pytesseract

with Image.open('../tests/sample_images/image_67178753.JPG') as img:
    dpi = img.info.get('dpi')
    print(dpi)
    print(pytesseract.image_to_osd(img))
    print(pytesseract.image_to_string(img))