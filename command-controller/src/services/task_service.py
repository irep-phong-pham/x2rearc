from src.constants import TaskStatus

from .base_service import BaseService
from src.exceptions import ErrorCode, WebAPIException
from src.daos import ConcreteFactory, FactoryInterface


class TaskService(BaseService):
    def __init__(self, dao_factory: FactoryInterface = None):
        super().__init__(dao_factory=dao_factory)
        self.task_dao = self.dao_factory.create_task_dao()

    def get_all_tasks(self):
        tasks = self.task_dao.get_all()
        return tasks

    def get_task(self, task_id):
        task = self.task_dao.get(id=task_id)
        if task is None:
            raise WebAPIException(ErrorCode.ITEM_NOT_FOUND)
        return task

    def add_task(self, title, description=None):
        # TODO: implement here
        return {'id': 1}

    def delete_task(self, task_id):
        # TODO: implement here
        pass
