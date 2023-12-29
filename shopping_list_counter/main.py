import cv2
import easyocr
import matplotlib.pyplot as plt
from typing import Optional
from urllib.request import urlopen
from urllib.parse import urlencode

import pandas as pd
from lxml import etree

from shopping_list_counter.models.cart import CartProduct, Cart
from shopping_list_counter.models.store_product import StoreProduct

path = 'example.png'
pd.set_option('display.max_columns', 999)
pd.set_option('display.width', 1000)

def main():
    print('Reading provided shopping list...')

    cart = Cart()
    cart.add_product(search_for_product_price('banan', '2KG'))
    cart.show()

def read_shopping_list(img_path: str):
    # TODO: Implement correct reading from list
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    plt.imshow(threshold)
    plt.show()

    reader = easyocr.Reader(['pl'])
    results = reader.readtext(img, decoder='wordbeamsearch', detail=0)

    print(results)
    return results

def search_for_product_price(product_name: str, quantity: Optional[str]) -> Optional[CartProduct]:
    print(f"Start searching for '{product_name}'...")
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
    frame_data = []

    for i in range(len(product_names)):
        name = product_names[i].text
        make = product_makes[i].text
        price = product_prices[i].text

        product = StoreProduct(name, make, price)
        frame_data.append([product.make, product.name, product.price_text, f'{product.weight} {product.unit}'])
        products.append(product)

    df = pd.DataFrame(frame_data, columns=['Make', 'Name', 'Price', 'Weight'])
    print(df, '\n')

    # TODO: Add possibility to skip product, if search result not satisfied
    selected = int(input('Which product would you like to buy?: '))
    print('')

    amount = None
    if quantity is not None:
        amount = products[selected].calc_amount_for_weight(quantity)

    if amount is None:
        amount = float(input('How much would you like to buy?: '))

    print('')
    return CartProduct.create_from_store_product(products[selected], amount)

main()
