from flask import request
from webargs import fields
from webargs.flaskparser import parser

from src.services import TaskService
from .anonymous_base_controller import AnonymousBaseController
from src.controllers.common.http_exceptions import HTTPNotFoundException, HTTPServerInternalException
from src.exceptions import WebAPIException, ErrorCode

from .schemas import TaskResponseSchema
from marshmallow import EXCLUDE

task_args = {
    # Required arguments
    "title": fields.Str(required=True),
    "description": fields.Str(required=False)
    # "camelCaseParam": fields.Str()
}


class TaskController(AnonymousBaseController):
    def __init__(self):
        super().__init__()
        self.task_service = TaskService()

    def get(self, id):
        try:
            task = self.task_service.get_task(task_id=id)
            return TaskResponseSchema().load(data=task, unknown=EXCLUDE)
        except WebAPIException as e:
            if e.code == ErrorCode.ITEM_NOT_FOUND:
                raise HTTPNotFoundException(
                    api_code='A001',
                    custom_message=f'Not found task with id={id}')
            else:
                raise HTTPServerInternalException()

    def post(self, args):
        args = parser.parse(task_args, request)
        task_id = self.task_service.add_task(title=args['title'],
                                             description=args['description'])
        return TaskResponseSchema(only=('id')).load(data={'id': task_id})

    def delete(self, id):
        task_id = self.task_service.delete_task(id)
        return TaskResponseSchema(only=('id')).load(data={'id': task_id})

    def put(self, id):
        pass

    def patch(self, id):
        pass
