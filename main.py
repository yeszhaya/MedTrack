from services.ConsoleInput import ConsoleInput
from services.CsvDataSaver import CsvDataSaver
from services.ConsoleNotifier import ConsoleNotifier
from services.Scheduler import Scheduler

RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def main():
    scheduler = Scheduler(
        input_source=ConsoleInput(),
        data_saver=CsvDataSaver(),
        notifier=ConsoleNotifier()
    )

    print(
        f"\n{CYAN}{'MEDTRACK':^50}\n"
        f"{'Personal Medication Reminder System':^50}{RESET}"
    )

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
            name_to_delete = input(
                "Enter exact medicine name to remove: "
            )

            scheduler.remove_medicine(name_to_delete)

        elif choice == "5":
            print(
                f"\n{CYAN}Application closed. "
                f"Stay healthy and remember your meds!{RESET}"
            )

            break

        else:
            print(
                f"{RED}Invalid option. "
                f"Please select numbers only between 1 to 5.{RESET}"
            )


if __name__ == "__main__":
    main()