import time
from urllib.request import urlopen

import cv2
from easyocr import easyocr
from lxml import etree

path = 'example.png'

def main():
    print('Reading countries from photo...')
    countries = read_countries(path)

    for country in countries:
        search_for_country_info(country)

def read_countries(img_path: str):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    reader = easyocr.Reader(['en'])
    results = reader.readtext(img, decoder='wordbeamsearch', detail=0)

    return results

def search_for_country_info(country_name: str):
    country_in_url = words_as_sentence(country_name).replace(' ','')
    url = f"https://www.countryreports.org/country/{country_in_url}/fact.htm"

    print(f'Searching info about `{words_as_sentence(country_name)}`...')
    print(f"Source: {url}\n")

    page = urlopen(url)
    html = page.read().decode("utf-8")
    dom = etree.HTML(str(html))

    td_list = dom.xpath('//*[@id="my-content"]/div/div/div/div[3]/div/div/table/tr/td')

    for i, j in pairwise(td_list):
        print(f"{i.text.strip()}: ")
        print(f"{j.text.strip()}\n")
        time.sleep(0.2)

    print('\nPress `Enter` to continue...')
    input()

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def words_as_sentence(text):
    result = ''
    for text in text.split(' '):
        result += f'{text[0].upper()}{text[1:]} '

    return result.strip()

main()
