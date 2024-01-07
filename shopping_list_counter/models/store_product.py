import re
import math
from typing import Optional

class StoreProduct(object):
    name: str
    make: str
    price: float
    price_text: str
    weight: Optional[float]
    unit: Optional[str]

    UNITS = [
        {'G': 1, 'DAG': 10, 'KG': 1000},
        {'L': 1, 'ML': 0.001},
        {'SZT': 1},
    ]

    def __init__(self, name: str, make: str, price_text: str):
        self.name = name
        self.make = make
        self.price_text = price_text.replace(',', '.')
        self.price = float(self.price_text[:-3])

        basis_weight = StoreProduct.detect_weight_and_unit(self.name)
        if basis_weight is None:
            self.weight, self.unit = None, None
        else:
            self.weight, self.unit = basis_weight

    def __str__(self):
        return f'[{self.make}] {self.name}: {self.price}'

    def can_buy_loose(self) -> bool:
        return self.weight is None and self.unit is not None

    def get_weight_text(self) -> str:
        if self.unit is None:
            return '-'

        if self.weight is None:
            return self.unit

        if self.weight.is_integer():
            return f'{self.weight:.0f} {self.unit}'

        return f'{self.weight:.2f} {self.unit}'

    def get_product_weight_in_basis_unit(self) -> Optional[list[float, str]]:
        if self.unit is None:
            return None

        return StoreProduct.transform_weight_for_basis_unit(self.weight, self.unit)

    def calc_amount_for_weight(self, weight_text: str) -> Optional[float]:
        parsed_weight = StoreProduct.detect_weight_and_unit(weight_text)
        if parsed_weight is None:
            return None

        weight, unit = parsed_weight
        basis_weight, basis_unit = StoreProduct.transform_weight_for_basis_unit(weight, unit)

        if weight.is_integer() and self.weight is not None and basis_unit == 'SZT':
            return weight

        product_basis_weight = self.get_product_weight_in_basis_unit()
        if product_basis_weight is None:
            return None

        product_weight, product_unit = product_basis_weight
        if product_unit != basis_unit:
            return None

        if self.can_buy_loose():
            return round(weight, 2)

        return int(math.ceil(basis_weight / product_weight))

    @staticmethod
    def transform_weight_for_basis_unit(weight: float, unit: str) -> Optional[list[float, str]]:
        base_units = None
        for unit_type in StoreProduct.UNITS:
            if unit in unit_type.keys():
                base_units = unit_type
                break

        if base_units is None:
            return None

        base_unit = list(base_units.keys())[0]
        if weight is None:
            return [None, base_unit]

        return [weight * base_units[unit], base_unit]

    @staticmethod
    def detect_weight_and_unit(text: str) -> Optional[list[float, str]]:
        match = re.search(r'\d*[,.]?\d+(KG|G|SZT|L|ML)', text)
        if match is None:
            if re.search(r'(1 SZT|1 PĘCZEK|\sSZTUKA)', text) is not None:
                return [1.0, 'SZT']
            if re.search(r'(\sKG|\sLUZ)', text) is not None:
                return [None, 'KG']
            return None

        temp = str(match.group(0))
        weight = float(re.search(r'^\d*[,.]?\d+', temp).group(0).replace(',', '.'))
        unit = re.search(r'[A-Z]+$', temp).group(0)
        return [weight, unit]
