from .factory_interface import FactoryInterface
from .task_dao import TaskDAOInterface, TaskDAO


class ConcreteFactory(FactoryInterface):
    def create_task_dao(self) -> TaskDAOInterface:
        return TaskDAO()
