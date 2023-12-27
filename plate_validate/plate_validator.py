from abc import ABC, abstractmethod
import re

class PlateValidator(ABC):
    full_plate: str
    discriminant: str
    plate: str

    def __init__(self, full_plate):
        self.full_plate = full_plate

    def __str__(self):
        return f'Plate: ({self.discriminant} {self.plate})'

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError

class TwoDigitDiscriminantPlateValidator(PlateValidator):
    correct_plates = (
        "^\d{5}$",
        "^\d{4}[A-Z]{1}$",
        "^\d{3}[A-Z]{2}$",
        "^\d{1}[A-Z]{1}[1-9]{1}\d{2}$",
        "^\d{1}[A-Z]{2}[1-9]{1}\d{1}$",
    )

    def __init__(self, full_plate):
        super().__init__(full_plate)

        assert len(full_plate) == 7, "Two digit discriminant plate must be 7 chars long"

        self.discriminant = full_plate[:2]
        self.plate =full_plate[2:]

    def validate(self) -> bool:
        if re.search(r"[A-Z]{2}", self.discriminant) is None:
            return False

        for expression in self.correct_plates:
            result = re.search(expression, self.plate)
            if result is not None:
                return True
        return False

class ThreeDigitDiscriminantPlateValidator(PlateValidator):
    correct_plates = (
        "^[A-Z]{1}\d{3}$",
        "^\d{2}[A-Z]{2}$",
        "^\d{1}[A-Z]{1}[1-9]{1}\d{1}$",
        "^\d{2}[A-Z]{1}[1-9]{1}$",
        "^[1-9]{1}[A-Z]{2}[1-9]{1}$",
        "^[A-Z]{2}\d{2}$",
        "^\d{5}$",
        "^\d{4}[A-Z]{1}$",
        "^\d{3}[A-Z]{2}$",
        "^[A-Z]{1}\d{2}[A-Z]{1}$",
        "^[A-Z]{1}[1-9]{1}[A-Z]{2}$",
    )

    def __init__(self, full_plate):
        super().__init__(full_plate)

        assert len(full_plate) == 7 or len(full_plate) == 8, "Three digit discriminant plate can be 7 or 8 chars long"

        self.discriminant = full_plate[:3]
        self.plate =full_plate[3:]

    def validate(self) -> bool:
        if re.search(r"[A-Z]{3}", self.discriminant) is None:
            return False

        for expression in self.correct_plates:
            result = re.search(expression, self.plate)
            if result is not None:
                return True
        return False

