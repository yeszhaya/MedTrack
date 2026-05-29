import csv
import os

from interfaces.IDataSaver import IDataSaver
from models.Medicine import Medicine

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


class CsvDataSaver(IDataSaver):

    def __init__(self, filename: str = "mymeds_history.csv"):
        self._filename = filename

        if not os.path.exists(self._filename):
            with open(
                self._filename,
                mode='w',
                newline='',
                encoding='utf-8'
            ) as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Dosage", "ScheduleTime"])

    def save_data(self, data: list) -> None:
        try:
            with open(
                self._filename,
                mode='w',
                newline='',
                encoding='utf-8'
            ) as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Dosage", "ScheduleTime"])

                for med in data:
                    writer.writerow([
                        med.name,
                        med.dosage,
                        med.intake_time
                    ])

            print(f"{GREEN}Data saved successfully to {self._filename}.{RESET}")

        except IOError as error:
            print(f"{RED}File handling error occurred: {str(error)}.{RESET}")

    def load_data(self) -> list:
        medicines_list = []

        try:
            with open(
                self._filename,
                mode='r',
                newline='',
                encoding='utf-8'
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        med = Medicine(
                            name=row["Name"],
                            dosage=row["Dosage"],
                            intake_time=row["ScheduleTime"]
                        )

                        medicines_list.append(med)

                    except ValueError:
                        continue

        except FileNotFoundError:
            print(
                f"{YELLOW}{self._filename} not found "
                f"— starting with empty record list.{RESET}"
            )

        except IOError as error:
            print(f"{RED}Error reading file: {str(error)}.{RESET}")

        return medicines_list