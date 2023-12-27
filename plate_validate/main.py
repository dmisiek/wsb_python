import cv2
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib.pyplot as plt
import easyocr
import pytesseract

from plate_validate.plate_validator import TwoDigitDiscriminantPlateValidator, ThreeDigitDiscriminantPlateValidator

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

IMAGE_PATH = 'example.png'

def detect_and_cut_plate(path: str):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blur image for easier shapes recognition
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    # transforming image for countour
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    plate_countour = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            plate_countour = approx
            break

    if plate_countour is None:
        print("No plate detected")
        return None

    # creating mask and fill with shape of plate
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [plate_countour], 0, (255, 255, 255), -1)

    # getting coords where mask is white
    x, y = np.where(mask == 255)
    topX, topY = (np.min(x), np.min(y))
    bottomX, bottomY = (np.max(x), np.max(y))

    # crop and save image
    cropped_image = gray[topX:bottomX, topY:bottomY]
    cropped_path = f'{path.split(".")[0]}_cropped.png'
    cv2.imwrite(cropped_path, cropped_image)

    return cropped_path

def recognize_plate_numbers(path: str):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # thresholding image for better recognition with ocr
    _, thresh = cv2.threshold(gray, 72, 255, cv2.THRESH_BINARY)

    # EasyOCR
    reader = easyocr.Reader(['en'])
    results = reader.readtext(thresh, detail=0)
    return ''.join(results)

    # pytesseract
    # result = pytesseract.image_to_string(thresh, config='--psm 7')
    # return result

# TODO: Implement plate validation
def validate_plate(plate: str):
    validator = ThreeDigitDiscriminantPlateValidator(plate)
    print(validator, validator.validate())

# TODO: Uncomment after plate validator will be full implemented
# cropped_path = detect_and_cut_plate(IMAGE_PATH)
# plate = recognize_plate_numbers(cropped_path)
# print(plate)

plate_validation = validate_plate('XY1AA04')
