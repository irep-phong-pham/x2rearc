from flask import request
from webargs import fields
from webargs.flaskparser import parser

from .anonymous_base_controller import AnonymousBaseController
from src.controllers.common.http_exceptions import (
    HTTPNotFoundException,
    HTTPServerInternalException,
)
from src.exceptions import WebAPIException, ErrorCode

from .schemas import TaskResponseSchema
from marshmallow import EXCLUDE
from src.services import PerformanceService


performance_args = {
    # Required arguments
    "id": fields.Str(required=True),
    "payload": fields.Str(required=True)
    # "camelCaseParam": fields.Str()
}


class PerformanceController(AnonymousBaseController):
    def __init__(self):
        super().__init__()
        self.performance_service = PerformanceService()

    def get(self):
        return "performance"

    def post(self, *args):
        args = parser.parse(performance_args, request)
        self.performance_service.add_performance(id=args["id"], payload=args["payload"])
        return "success"
