"""
Refs: https://marshmallow.readthedocs.io/en/stable/
"""

from marshmallow import fields, validate
from src.constants import TaskStatus
from src.utils import helper
from .base_response_schema import BaseResponseSchema


class TaskResponseSchema(BaseResponseSchema):
    id = fields.Int(required=False)
    name = fields.String(required=True)
    description = fields.String(required=False, allow_none=True, default=None)
    # status = fields.String(required=True,  default=TaskStatus.TODO, validate=validate.OneOf((helper.get_all_constants_values(TaskStatus))))
    # user_id = fields.Int(required=True)
