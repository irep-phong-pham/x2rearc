from abc import ABC, abstractmethod


class TaskDAOInterface(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass
