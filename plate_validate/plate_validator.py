import os.path
from abc import ABC, abstractmethod
import re

class PlateValidator(ABC):
    plate: str

    def __init__(self, plate):
        self.plate = plate

    def __str__(self):
        return f'Plate: ({self.plate})'

    @abstractmethod
    def get_correct_plate_expressions(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def is_correct_length(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_correct_region_code(self) -> bool:
        raise NotImplementedError

    def validate(self) -> bool:
        if not self.is_correct_length():
            return False

        if not self.is_correct_region_code():
            return False

        for expression in self.get_correct_plate_expressions():
            result = re.search(expression, self.plate)
            if result is not None:
                return True

        return False

class TwoDigitRegionCodePlateValidator(PlateValidator):
    def __init__(self, plate):
        assert os.path.isfile('two-digit-region-codes.txt'), "TwoDigitRegionCodePlateValidator require `two-digit-region-codes.txt` file to work properly"
        super().__init__(plate)

    def get_correct_plate_expressions(self) -> list:
        return [
            "^[A-Z]{2}\d{5}$",
            "^[A-Z]{2}\d{4}[ACE-HJ-NP-Y]{1}$",
            "^[A-Z]{2}\d{3}[ACE-HJ-NP-Y]{2}$",
            "^[A-Z]{2}\d{1}[ACE-HJ-NP-Y]{1}[1-9]{1}\d{2}$",
            "^[A-Z]{2}\d{1}[ACE-HJ-NP-Y]{2}[1-9]{1}\d{1}$",
        ]

    def is_correct_length(self) -> bool:
        return len(self.plate) == 7

    def is_correct_region_code(self) -> bool:
        with open('two-digit-region-codes.txt', mode='r') as f:
            region_codes = f.read().splitlines()

        region_code = self.plate[:2]
        return region_code in region_codes

class ThreeDigitRegionCodePlateValidator(PlateValidator):
    def __init__(self, plate):
        assert os.path.isfile('three-digit-region-codes.txt'), "ThreeDigitRegionCodePlateValidator require `three-digit-region-codes.txt` file to work properly"
        super().__init__(plate)

    def get_correct_plate_expressions(self) -> list:
        return [
            "^[A-Z]{3}[ACE-HJ-NP-Y]{1}\d{3}$",
            "^[A-Z]{3}\d{2}[ACE-HJ-NP-Y]{2}$",
            "^[A-Z]{3}\d{1}[ACE-HJ-NP-Y]{1}[1-9]{1}\d{1}$",
            "^[A-Z]{3}\d{2}[ACE-HJ-NP-Y]{1}[1-9]{1}$",
            "^[A-Z]{3}[1-9]{1}[ACE-HJ-NP-Y]{2}[1-9]{1}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{2}\d{2}$",
            "^[A-Z]{3}\d{5}$",
            "^[A-Z]{3}\d{4}[ACE-HJ-NP-Y]{1}$",
            "^[A-Z]{3}\d{3}[ACE-HJ-NP-Y]{2}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{1}\d{2}[ACE-HJ-NP-Y]{1}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{1}[1-9]{1}[ACE-HJ-NP-Y]{2}$",
        ]

    def is_correct_length(self) -> bool:
        return len(self.plate) in [7, 8]

    def is_correct_region_code(self) -> bool:
        with open('three-digit-region-codes.txt', mode='r') as f:
            region_codes = f.read().splitlines()

        region_code = self.plate[:3]
        return region_code in region_codes

class MotorPlateValidator(PlateValidator):
    def __init__(self, plate):
        assert os.path.isfile('two-digit-region-codes.txt'), "TwoDigitRegionCodePlateValidator require `two-digit-region-codes.txt` file to work properly"
        assert os.path.isfile('three-digit-region-codes.txt'), "ThreeDigitRegionCodePlateValidator require `three-digit-region-codes.txt` file to work properly"
        super().__init__(plate)

    def get_correct_plate_expressions(self) -> list:
        return [
            "^[A-Z]{2}\d{4}$",
            "^[A-Z]{2}\d{3}[ACE-HJ-NP-Y]{1}$",
            "^[A-Z]{2}\d{2}[ACE-HJ-NP-Y]{1}[1-9]{1}$",
            "^[A-Z]{2}[1-9]{1}[ACE-HJ-NP-Y]{1}\d{2}$",
            "^[A-Z]{2}[ACE-HJ-NP-Y]{1}\d{3}$",
            "^[A-Z]{2}\d{2}[ACE-HJ-NP-Y]{2}$",
            "^[A-Z]{2}[1-9]{1}[ACE-HJ-NP-Y]{2}[1-9]{1}$",
            "^[A-Z]{2}[ACE-HJ-NP-Y]{2}\d{2}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{1}\d{3}$",
            "^[A-Z]{3}\d{2}[ACE-HJ-NP-Y]{2}$",
            "^[A-Z]{3}\d{1}[ACE-HJ-NP-Y]{1}[1-9]{1}\d{1}$",
            "^[A-Z]{3}\d{2}[ACE-HJ-NP-Y]{1}[1-9]{1}$",
            "^[A-Z]{3}[1-9]{1}[ACE-HJ-NP-Y]{2}[1-9]{1}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{2}\d{2}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{1}\d{2}[ACE-HJ-NP-Y]{1}$",
            "^[A-Z]{3}[ACE-HJ-NP-Y]{1}[1-9]{1}[ACE-HJ-NP-Y]{2}$",
        ]

    def is_correct_length(self) -> bool:
        return len(self.plate) in [6, 7]

    def is_correct_region_code(self) -> bool:
        with open('two-digit-region-codes.txt', mode='r') as f:
            region_codes = f.read().splitlines()

        region_code = self.plate[:2]
        if region_code in region_codes:
            return True

        with open('three-digit-region-codes.txt', mode='r') as f:
            region_codes = f.read().splitlines()

        region_code = self.plate[:3]
        return region_code in region_codes

class ReducedPlateValidator(PlateValidator):
    def get_correct_plate_expressions(self) -> list:
        return [
            "^[A-Z]{1}\d{3}$",
            "^[A-Z]{1}\d{2}[ACE-HJ-NP-Y]{1}$",
            "^[A-Z]{1}[1-9]{1}[ACE-HJ-NP-Y]{1}[1-9]{1}$",
            "^[A-Z]{1}[ACE-HJ-NP-Y]{1}\d{2}$",
            "^[A-Z]{1}[1-9]{1}[ACE-HJ-NP-Y]{2}$",
            "^[A-Z]{1}[ACE-HJ-NP-Y]{2}[1-9]{1}$",
            "^[A-Z]{1}[ACE-HJ-NP-Y]{1}[1-9]{1}[ACE-HJ-NP-Y]{1}$",
        ]

    def is_correct_length(self) -> bool:
        return len(self.plate) == 4

    def is_correct_region_code(self) -> bool:
        region_code = self.plate[:1]
        return re.search('^[B-GI-PR-TV-Z]$', region_code) is not None
