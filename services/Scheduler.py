from datetime import datetime

from interfaces.IInputSource import IInputSource
from interfaces.IDataSaver import IDataSaver
from interfaces.INotifier import INotifier
from models.Medicine import Medicine

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


class Scheduler:
    def __init__(
        self,
        input_source: IInputSource,
        data_saver: IDataSaver,
        notifier: INotifier
    ):
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

            print(
                f"{GREEN}'{new_medicine.name}' "
                f"successfully added to schedule!{RESET}"
            )

        except ValueError as error:
            print(f"{RED}Invalid entry: {str(error)}.{RESET}")

    def remove_medicine(self, med_name: str) -> None:
        for index, med in enumerate(self._medicines):
            if med.name.lower() == med_name.strip().lower():
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

        print(f"\n{CYAN}{'ALL SCHEDULED MEDICINES':^50}{RESET}")
        print("=" * 50)

        for count, med in enumerate(self._medicines, 1):
            print(f"{count}. Name     : {med.name}")
            print(f"   Dosage   : {med.dosage}")
            print(f"   Time     : {med.intake_time}")
            print("-" * 50)