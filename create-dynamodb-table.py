import boto3
from botocore import exceptions
import random
import time
from pprint import pprint

# 対象のテーブル
table_names = [
    "event",
    "event_provider",
]

# 初期化
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
boto3.setup_default_session(
    aws_access_key_id="dummy",  # ローカルといえども何かを送る必要あるので値は適当
    aws_secret_access_key="dummy",  # 同上
    region_name="us-east-1",
)
endpoint_url = "http://localhost:8000"
cli_dynamo = boto3.client("dynamodb", endpoint_url=endpoint_url)

# テスト用にテーブル作成
res = cli_dynamo.create_table(
    TableName=table_names[0],
    KeySchema=[
        {"AttributeName": "id", "KeyType": "HASH"},
        {"AttributeName": "payload", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "id", "AttributeType": "S"},
        {"AttributeName": "payload", "AttributeType": "S"},
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    StreamSpecification={
        "StreamEnabled": True,
        "StreamViewType": "NEW_AND_OLD_IMAGES",
    },
)
print(f"[create_table] table_name={table_names[0]}")
pprint(res)
print("")
