import easyocr

PHOTO_PATH = 'example.jpg'

reader = easyocr.Reader(['en'])
result = reader.readtext(PHOTO_PATH)
print(result)