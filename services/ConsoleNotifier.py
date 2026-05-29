from interfaces.INotifier import INotifier

CYAN = "\033[96m"
RESET = "\033[0m"


class ConsoleNotifier(INotifier):

    def notify(self, message: str) -> None:
        print(f"\n{CYAN}{'MEDICATION REMINDER':^50}{RESET}")
        print("=" * 50)
        print(message)
        print("-" * 50 + "\n")