from abc import ABC, abstractmethod


class IInputSource(ABC):

    @abstractmethod
    def get_input(self) -> dict:
        pass