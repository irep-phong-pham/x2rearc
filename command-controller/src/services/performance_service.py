from src.constants import TaskStatus

from .base_service import BaseService
from src.exceptions import ErrorCode, WebAPIException
from src.daos import ConcreteFactory, FactoryInterface
import boto3
import os


class PerformanceService(BaseService):
    def __init__(self, dao_factory: FactoryInterface = None):
        super().__init__(dao_factory=dao_factory)

    def add_performance(self, id, payload):
        # TODO: implement here
        table_name = "event"
        boto3.setup_default_session(
            aws_access_key_id="dummy",  # ローカルといえども何かを送る必要あるので値は適当
            aws_secret_access_key="dummy",  # 同上
            region_name="us-east-1",
        )
        endpoint_url = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000")
        cli_dynamo = boto3.client("dynamodb", endpoint_url=endpoint_url)
        item = {
            "id": {"S": id},
            "payload": {"S": payload},
        }
        res = cli_dynamo.put_item(
            TableName=table_name,
            Item=item,
        )
        print(f"[put_item] table_name={table_name}, item={item}")
        print(res)
        print("")
