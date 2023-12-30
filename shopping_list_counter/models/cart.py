from shopping_list_counter.models.store_product import StoreProduct
import pandas as pd
import math

class CartProduct(object):
    name: str
    make: str
    price: float
    amount: float

    def __init__(self, name: str, make: str, price: float, amount: float):
        self.name = name
        self.make = make
        self.price = float(price)
        assert amount > 0, "Amount must be at least 0.1 to arrive on shopping list"
        self.amount = float(amount)

    @staticmethod
    def create_from_store_product(product: StoreProduct, amount: float):
        return CartProduct(
            name=product.name,
            make=product.make,
            price=product.price,
            amount=amount,
        )

    def get_total_price(self) -> float:
        return math.ceil(self.amount * self.price * 100) / 100

class Cart(object):
    products: list[CartProduct]

    def __init__(self):
        self.products = []

    def add_product(self, product: CartProduct):
        assert product is not CartProduct, "`product` must be class of CartProduct"
        self.products.append(product)

    def get_total_price(self) -> float:
        total_price = sum(map(lambda x: x.get_total_price(), self.products))
        return math.ceil(total_price * 100) / 100

    def show(self):
        frame_data = []
        for product in self.products:
            frame_data.append([product.make, product.name, f'{product.price} zł', product.amount, f'{product.get_total_price()} zł'])

        frame_data.append(['','','','', f'{self.get_total_price()} zł'])
        df = pd.DataFrame(frame_data, columns=['Make', 'Name', 'Price', 'Amount', 'Total price'])

        print('\nCurrent state of cart: ')
        print(df)

    def show_on_chart(self):
        # TODO: Implement showing products shares on chart
        pass


