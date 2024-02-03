from geopy.geocoders import Nominatim
import cv2
import easyocr

def main():
    image_path = 'example.png'
    country_names = read_country_names(image_path)

    for country_name in country_names:
        # assuming every city on map starts with upper case
        if not country_name[0].isupper():
            continue

        search_details(country_name)

def read_country_names(img_path: str):
    print(f'Reading country names from {img_path}...\n')

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    reader = easyocr.Reader(['pl'])
    results = reader.readtext(img, detail=0)

    return results


def search_details(city_name: str):
    geocoder = Nominatim(user_agent="map_reader")
    localization = geocoder.geocode(city_name)

    if localization is not None:
        print(f'Location: {city_name}, {localization.latitude}, {localization.longitude} (lat, lng)\n')
    else:
        print(f'"{city_name}" - No location found\n')

main()
