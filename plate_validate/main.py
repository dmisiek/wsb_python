import os
from typing import Optional

import cv2
import numpy as np
import easyocr

from plate_validate.plate_validator import ThreeDigitRegionCodePlateValidator, TwoDigitRegionCodePlateValidator, \
    ReducedPlateValidator, MotorPlateValidator

def main():
    image_path = 'example.png'

    if not os.path.isfile(image_path):
        raise FileNotFoundError(f'{image_path} not exists or path is incorrect.')

    print("Start detecting car's plate...")
    cropped_path = detect_and_cut_plate(image_path)

    if cropped_path is None:
        print("No car's plate detected")
        return

    print(f"Potential car plate detected and saved [{cropped_path}]")

    print("Start recognizing plate license numbers...")
    plate = recognize_plate_numbers(cropped_path)

    print(f"Validating plate '{plate}'...")
    result = 'valid' if validate_plate(plate) else 'invalid'

    print(f'Plate {plate} is {result}')

def detect_and_cut_plate(path: str) -> Optional[str]:
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # blur image for easier shapes recognition
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    # transforming image for contours
    edged = cv2.Canny(gray, 30, 200)

    # preparing contours
    img_contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = sorted(img_contours, key=cv2.contourArea, reverse=True)
    plate_contour = None

    # searching for 4 vertices polygon
    for c in img_contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            plate_contour = approx
            break

    if plate_contour is None:
        return None

    # creating mask and fill with shape of plate
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [plate_contour], 0, (255, 255, 255), -1)

    # getting coords where mask is white
    x, y = np.where(mask == 255)
    top_x, top_y = (np.min(x), np.min(y))
    bottom_x, bottom_y = (np.max(x), np.max(y))

    # crop and save image
    cropped_image = gray[top_x:bottom_x, top_y:bottom_y]
    cropped_path = f'{path.split(".")[0]}_cropped.png'
    cv2.imwrite(cropped_path, cropped_image)

    return cropped_path

def recognize_plate_numbers(path: str) -> str:
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # thresholding image for better recognition with ocr
    _, thresh = cv2.threshold(gray, 72, 255, cv2.THRESH_BINARY)

    reader = easyocr.Reader(['en'])
    results = reader.readtext(thresh, detail=0)

    car_plate = ''.join(results).replace(' ', '')
    car_plate.capitalize()

    return car_plate

def validate_plate(car_plate: str):
    # TODO: Add validator for TemporaryPlates, SafetyInstitutions
    for validator in [
        ThreeDigitRegionCodePlateValidator,
        TwoDigitRegionCodePlateValidator,
        MotorPlateValidator,
        ReducedPlateValidator,
    ]:
        try:
            v = validator(car_plate)
            valid = v.validate()

            if valid:
                return True
        except AssertionError:
            pass

    return False

main()
