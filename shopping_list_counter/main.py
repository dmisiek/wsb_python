import cv2
import easyocr
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
    products = read_shopping_list(path)
    shopping_list = []

    for item in products:
        tmp = StoreProduct.detect_weight_and_unit(item)

        if tmp is not None:
            if float(tmp[0]).is_integer():
                unit = f'{tmp[0]:.0f}{tmp[1]}'
            else:
                unit = f'{tmp[0]}{tmp[1]}'

            shopping_list.append({
                'name': item.replace(unit, '').strip(),
                'quantity': unit
            })
        else:
            shopping_list.append({
                'name': item.strip(),
                'quantity': None,
            })

        print(shopping_list[-1])


    cart = Cart()
    for item in shopping_list:
        product = search_for_product(item['name'], item['quantity'])
        if product is not None:
            cart.add_product(product)

    cart.show()
    cart.show_on_chart()

def read_shopping_list(img_path: str):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    reader = easyocr.Reader(['pl'])
    results = reader.readtext(img, detail=0)

    return results

def search_for_product(product_name: str, quantity: Optional[str]) -> Optional[CartProduct]:
    print(f"\nStart searching for '{product_name}'...")
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

    if len(product_names) == 0:
        print(f"Product '{product_name}' not found!")
        return None

    products = []
    frame_data = []

    for i in range(len(product_names)):
        name = product_names[i].text
        make = product_makes[i].text
        price = product_prices[i].text

        product = StoreProduct(name, make, price)
        frame_data.append([product.make, product.name, product.price_text, product.get_weight_text()])
        products.append(product)

    frame_data.append(['SKIP PRODUCT', '', '', ''])
    df = pd.DataFrame(frame_data, columns=['Make', 'Name', 'Price', 'Weight'])
    print(df, '\n')

    while True:
        try:
            selected = int(input('Which product would you like to buy? '))
            if 0 <= selected <= len(products):
                break

            raise ValueError
        except ValueError:
            print(f'Enter correct value from range 0-{len(products)}! \n')
            continue

    if selected == len(products):
        print('Skipping this product...')
        return None

    amount = None
    if quantity is not None:
        amount = products[selected].calc_amount_for_weight(quantity)

    if amount is None:
        while True:
            try:
                amount = float(input('How much would you like to buy?: '))

                if amount <= 0:
                    raise ValueError

                if products[selected].can_buy_loose():
                    break

                if amount.is_integer():
                    break

                print("This product doesn't support partial amounts!")
            except ValueError:
                print(f'Enter correct amount, greater than 0')
                continue

    return CartProduct.create_from_store_product(products[selected], amount)

main()
