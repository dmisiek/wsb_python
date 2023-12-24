import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2

PHOTO_PATH = 'example.png'
CUT_PHOTO_PATH = f'{PHOTO_PATH.split(".")[0]}_cut.png'

def get_plate(image: Image.Image) -> str:
    pic = np.array(image)

    saturation = 24
    saturation_main = 48

    mask = (pic[:,:,0] > 40) | ((pic[:, :, 1] < 60) & (pic[:, :, 1] > 120)) | ((pic[:, :, 2] < 160) & (pic[:, :, 2] > 230))
    pic[mask] = 255

    Image.fromarray(pic).save(CUT_PHOTO_PATH)

    reader = easyocr.Reader(['en'])
    # TODO: Expand bounding box to always read plate as one text
    results = reader.readtext(CUT_PHOTO_PATH)

    result_plate = ''

    for result in results:
        result_plate += result[1]
        # cv2.rectangle(pic, [int(result[0][0][0]), int(result[0][0][1])], [int(result[0][2][0]), int(result[0][2][1])], (255, 0, 0), 5)

    plt.imshow(pic)
    plt.show()
    return result_plate

def polish_plate_validation(plate: str) -> bool:
    pass


image = Image.open(PHOTO_PATH)
plate = get_plate(image)
print(plate)
