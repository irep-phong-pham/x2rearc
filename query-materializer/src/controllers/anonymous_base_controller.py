import flask_restful
from flask_restful import Api, output_json

class AnonymousBaseController(flask_restful.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__()
