from datetime import datetime
import re


class Medicine:
    def __init__(self, name: str, dosage: str, intake_time: str):
        self._name = None
        self._dosage = None
        self._intake_time = None
        self.name = name
        self.dosage = dosage
        self.intake_time = intake_time

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        clean = value.strip()

        if not clean:
            raise ValueError("Medicine name cannot be blank.")

        self._name = clean

    @property
    def dosage(self) -> str:
        return self._dosage

    @dosage.setter
    def dosage(self, value: str) -> None:
        clean = value.strip()

        if not clean:
            raise ValueError("Dosage cannot be blank.")

        numbers = re.findall(r'-?\d+\.?\d*', clean)

        if not numbers:
            raise ValueError("Dosage must contain a numeric value.")

        for n in numbers:
            if float(n) <= 0:
                raise ValueError("Dosage must be a positive value.")

        self._dosage = clean

    @property
    def intake_time(self) -> str:
        return self._intake_time

    @intake_time.setter
    def intake_time(self, value: str) -> None:
        try:
            datetime.strptime(value.strip(), "%H:%M")

        except ValueError:
            raise ValueError("Time must follow HH:MM 24-hour format.")

        self._intake_time = value.strip()

    def is_due(self, current_time: str) -> bool:
        return current_time == self._intake_time