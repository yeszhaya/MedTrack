from abc import ABC, abstractmethod
from datetime import datetime
import csv
import os
import re

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

class IInputSource(ABC):

    @abstractmethod
    def get_input(self) -> dict:
        pass


class IDataSaver(ABC):
 
    @abstractmethod
    def save_data(self, data: list) -> None:
        pass

    @abstractmethod
    def load_data(self) -> list:
        pass


class INotifier(ABC):

    @abstractmethod
    def notify(self, message: str) -> None:
        pass

class ConsoleInput(IInputSource):

    def get_input(self) -> dict:
        print(f"\n{CYAN}{'ADD NEW MEDICINE RECORD':^50}{RESET}")
        print("=" * 50)

        while True:
            name = input("Enter medicine name: ").strip()
            if name:
                break
            print(f"{RED}Error: Medicine name cannot be empty. Please try again.{RESET}")

        while True:
            dosage = input("Enter dosage (e.g 500mg / 1 tablet): ").strip()
            if dosage:
                break
            print(f"{RED}Error: Dosage cannot be empty. Please try again.{RESET}")

        while True:
            time_str = input("Enter schedule time (HH:MM, 24-hour format): ").strip()
            try:
                datetime.strptime(time_str, "%H:%M")
                break
            except ValueError:
                print(f"{RED}Error: Invalid time format. Please use HH:MM, example: 08:30, 14:00.{RESET}")

        return {"name": name, "dosage": dosage, "schedule_time": time_str}


class ConsoleNotifier(INotifier):

    def notify(self, message: str) -> None:
        print(f"\n{CYAN}{'MEDICATION REMINDER':^50}{RESET}")
        print("=" * 50)
        print(message)
        print("-" * 50 + "\n")

class CsvDataSaver(IDataSaver):
  
    def __init__(self, filename: str = "mymeds_history.csv"):
        self._filename = filename
        if not os.path.exists(self._filename):
            with open(self._filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Dosage", "ScheduleTime"])

    def save_data(self, data: list) -> None:
        try:
            with open(self._filename, mode='w', newline='', encoding='utf-8') as file:
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
            with open(self._filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    med = Medicine(
                        name=row["Name"],
                        dosage=row["Dosage"],
                        intake_time=row["ScheduleTime"]
                    )
                    medicines_list.append(med)
        except FileNotFoundError:
            print(f"{YELLOW}{self._filename} not found — starting with empty record list.{RESET}")
        except IOError as error:
            print(f"{RED}Error reading file: {str(error)}.{RESET}")
        return medicines_list

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

        numbers = re.findall(r'\d+\.?\d*', clean)
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
        return current_time >= self._intake_time

class Scheduler:

    def __init__(self, input_source: IInputSource, data_saver: IDataSaver, notifier: INotifier):
        self._input_source = input_source
        self._data_saver = data_saver
        self._notifier = notifier
        self._medicines: list[Medicine] = []
        self._load_existing_data()

    def _load_existing_data(self) -> None:
        self._medicines = self._data_saver.load_data()

    def add_medicine(self) -> None:
        try:
            med_data = self._input_source.get_input()
            new_medicine = Medicine(
                name=med_data["name"],
                dosage=med_data["dosage"],
                intake_time=med_data["schedule_time"]
            )
            self._medicines.append(new_medicine)
            self._data_saver.save_data(self._medicines)
            print(f"{GREEN}'{new_medicine.name}' successfully added to schedule!{RESET}")
        except ValueError as error:
            print(f"{RED}Invalid entry: {str(error)}.{RESET}")

    def remove_medicine(self, med_name: str) -> None:
        for index, med in enumerate(self._medicines):
            if med.name.lower() == med_name.lower():
                self._medicines.pop(index)
                self._data_saver.save_data(self._medicines)
                print(f"{GREEN}'{med_name}' removed from list.{RESET}")
                return    
        print(f"{YELLOW}Medicine named '{med_name}' not found.{RESET}")

    def check_schedules(self) -> None:
        now_time = datetime.now().strftime("%H:%M")
        
        print(f"\n{CYAN}{f'Current System Time: {now_time}':^50}{RESET}")

        for med in self._medicines:
            if med.is_due(now_time):
                message = (
                    f"TIME TO TAKE YOUR MEDICINE!\n"
                    f"Name: {med.name}\n"
                    f"Dosage: {med.dosage}\n"  
                    f"Schedule: {med.intake_time}"
                )
                self._notifier.notify(message)

    def view_all_medicines(self) -> None:
        if not self._medicines:
            print(f"\n{YELLOW}No medicine records found.{RESET}")
            return

        print(f"\n{CYAN}{f'ALL SCHEDULED MEDICINES':^50}{RESET}")
        print("=" * 50)
        for count, med in enumerate(self._medicines, 1):
            print(f"{count}.  Name     : {med.name}")
            print(f"    Dosage   : {med.dosage}")
            print(f"    Time     : {med.intake_time}")
            print("-" * 50)

def main():
    scheduler = Scheduler(
        input_source=ConsoleInput(),
        data_saver=CsvDataSaver(),
        notifier=ConsoleNotifier()
    )
    
    print(f"\n{CYAN}{'MEDICINE TRACKER':^50}\n{'Personal Medication Reminder System':^50}{RESET}")
    
    while True:
        print("\n" + "=" * 50)
        print(f"{'MAIN MENU':^50}")
        print("=" * 50)
        print("[1] Add New Medicine Schedule")
        print("[2] View All Medicine Records")
        print("[3] Check Due Medications Now")
        print("[4] Remove Medicine Record")
        print("[5] Exit Application")
        print("=" * 50)

        choice = input("Please enter your choice [1-5]: ").strip()

        if choice == "1":
            scheduler.add_medicine()
        elif choice == "2":
            scheduler.view_all_medicines()
        elif choice == "3":
            scheduler.check_schedules()
        elif choice == "4":
            name_to_delete = input("Enter exact medicine name to remove: ")
            scheduler.remove_medicine(name_to_delete)
        elif choice == "5":
            print(f"\n{CYAN}Application closed. Stay healthy and remember your meds!{RESET}")
            break
        else:
            print(f"{RED}Invalid option. Please select numbers only between 1 to 5.{RESET}")

if __name__ == "__main__":
    main()