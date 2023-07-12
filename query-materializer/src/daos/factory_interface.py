from abc import ABC, abstractmethod
from .task_dao import TaskDAOInterface


class FactoryInterface(ABC):
    @abstractmethod
    def create_task_dao(self) -> TaskDAOInterface:
        pass
