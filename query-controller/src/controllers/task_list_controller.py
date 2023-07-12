from .anonymous_base_controller import AnonymousBaseController
from src.services import TaskService
from .schemas import TaskResponseSchema
from marshmallow import EXCLUDE


class TaskListController(AnonymousBaseController):
    def get(self):
        task_svc = TaskService()
        tasks = task_svc.get_all_tasks()
        return TaskResponseSchema(many=True).load(tasks, unknown=EXCLUDE)
