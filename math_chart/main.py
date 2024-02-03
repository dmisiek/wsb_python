import matplotlib.pyplot as plt
import numpy as np
import cv2
import easyocr

def main():
    image_path = 'example.png'
    function = read_math_function(image_path)
    draw_math_function(function)

def read_math_function(img_path: str):
    print(f'Reading math function from {img_path}...\n')

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    reader = easyocr.Reader(['en'])
    results = reader.readtext(img, detail=0)

    return results[0]

def calc_value_for_argument(fx: str, x: int) -> int:
    if '=' in fx:
        fx = fx.replace(" ", "").split('=')[1]

    value_list = [fx]
    for mark in '*/+-':
        tmp = []
        for segment in value_list:
            segment = segment.split(mark)
            i = 0
            while i < len(segment):
                if i % 2 == 1:
                    segment.insert(i, mark)
                i += 1
            tmp += segment
        value_list = tmp

    i = 0
    while i < len(value_list):
        if 'x' not in value_list[i]:
            i += 1
            continue


        if len(value_list[i]) == 1:
            value_list[i] = f'{x}'
            i += 2
            continue

        value_list[i] = value_list[i].split('x')[0]
        value_list.insert(i + 1, '*')
        value_list.insert(i + 2, f'{x}')
        i += 3

    for marks in ['*/', '+-']:
        i = 0
        while i < len(value_list) - 1:
            if value_list[i + 1] not in marks:
                i += 2
                continue

            if value_list[i + 1] == '*':
                value_list[i] = float(value_list[i]) * float(value_list[i + 2])

            if value_list[i + 1] == '/':
                value_list[i] = float(value_list[i]) / float(value_list[i + 2])

            if value_list[i + 1] == '+':
                value_list[i] = float(value_list[i]) + float(value_list[i + 2])

            if value_list[i + 1] == '-':
                value_list[i] = float(value_list[i]) - float(value_list[i + 2])

            if len(value_list) != 1:
                del value_list[i + 2]
                del value_list[i + 1]


    if len(value_list) != 1:
        raise Exception('Something went wrong during calculating the value')

    return value_list[0]

def draw_math_function(function: str):
    print(f"Drawing math function '{function}' chart...")

    ax = plt.axes()
    ax.grid(True, which='both')
    ax.axhline(0, color='black', linewidth=.5)
    ax.axvline(0, color='black', linewidth=.5)

    x = np.linspace(-10, 10, 100)

    y_min = calc_value_for_argument(function, -10)
    y_max = calc_value_for_argument(function, 10)

    ax.plot(x, np.linspace(y_min, y_max, 100), linewidth=3)
    plt.show()

main()
