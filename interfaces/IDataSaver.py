from abc import ABC, abstractmethod


class IDataSaver(ABC):

    @abstractmethod
    def save_data(self, data: list) -> None:
        pass

    @abstractmethod
    def load_data(self) -> list:
        pass