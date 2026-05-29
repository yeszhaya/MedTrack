from datetime import datetime
import re

from interfaces.IInputSource import IInputSource

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


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

            if not dosage:
                print(f"{RED}Error: Dosage cannot be empty. Please try again.{RESET}")
                continue

            numbers = re.findall(r'-?\d+\.?\d*', dosage)

            if not numbers:
                print(f"{RED}Error: Dosage must contain a numeric value.{RESET}")
                continue

            invalid = False

            for n in numbers:
                if float(n) <= 0:
                    print(f"{RED}Error: Dosage must be a positive value.{RESET}")
                    invalid = True
                    break

            if not invalid:
                break

        while True:
            time_str = input("Enter schedule time (HH:MM, 24-hour format): ").strip()

            try:
                datetime.strptime(time_str, "%H:%M")
                break

            except ValueError:
                print(
                    f"{RED}Error: Invalid time format. "
                    f"Please use HH:MM, example: 08:30, 14:00.{RESET}"
                )

        return {
            "name": name,
            "dosage": dosage,
            "schedule_time": time_str
        }