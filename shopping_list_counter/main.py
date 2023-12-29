from typing import Optional

import cv2
import easyocr
import matplotlib.pyplot as plt
from urllib.request import urlopen
from urllib.parse import urlencode
from lxml import etree
from sympy.concrete import products

from shopping_list_counter.product import Product

path = 'example.png'



def main():
    print('Reading provided shopping list...')

    search_for_product_price('kajzerka', '5SZT')
    search_for_product_price('mleko 3,5%', '2L')
    search_for_product_price('banan', '1KG')

def read_shopping_list(path: str):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    plt.imshow(threshold)
    plt.show()

    reader = easyocr.Reader(['pl'])
    results = reader.readtext(img, decoder='wordbeamsearch', detail=0)

    print(results)
    return results

def search_for_product_price(product_name: str, quantity: Optional[str]):
    base_url = "https://intermarchebochnia.pl/szukaj"
    params = {
        'controller': 'search',
        's': product_name,
    }
    page = urlopen(f'{base_url}?{urlencode(params)}')
    html = page.read().decode("utf-8")
    dom = etree.HTML(str(html))


    product_names = dom.xpath('//*[@id="js-product-list"]/div/div/article/div[2]/div[1]/h3/a')
    product_makes = dom.xpath('//*[@id="js-product-list"]/div/div/article/div[2]/div[1]/div[1]/a')
    product_prices = dom.xpath('//*[@id="js-product-list"]/div/div/article/div[2]/div[1]/div[3]/span[2]')

    products = []

    for i in range(len(product_names)):
        name = product_names[i].text
        make = product_makes[i].text
        price = product_prices[i].text

        product = Product(name, make, price)
        print(f'{i}. {product}')
        products.append(product)

    selected = int(input('Which product would you like to buy?: '))

    amount = None
    if quantity is not None:
        amount = products[selected].calc_amount_for_weight(quantity)

    if amount is None:
        amount = int(input('How much would you like to buy?: '))


    print(f'Selected {amount} x {products[selected].name}')

main()
