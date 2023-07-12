import i18n
from pathlib import Path
import os
import boto3
import time
from pprint import pprint

# setup i18n
i18n.load_path.append(Path(__file__).parent.joinpath("locales"))
i18n.set("filename_format", "{locale}.{format}")
i18n.set("locale", os.getenv("LOCALE", "jp"))
i18n.set("enable_memoization", True)

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from src.config import Config
from src.database import Database
from src.controllers import (
    HealthyController,
    TaskController,
    TaskListController,
    PerformanceController,
)


def create_app():
    from src.controllers.common import errors

    # flask app config
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    Database(app=app)
    app.app_context().push()
    api = Api(app, errors=errors.errors)

    # Register api endpoint
    api.add_resource(HealthyController, "/healthy")
    api.add_resource(TaskListController, "/tasks")
    api.add_resource(TaskController, "/tasks/<int:id>")
    api.add_resource(PerformanceController, "/performances")

    flask_restfull_default_handle_error = api.handle_error

    def webapi_default_error_handler(error):
        """Default error handler"""
        try:
            if error.custom_message is not None:
                if error.api_code is not None:
                    code = "{}.{}".format(
                        error.api_code, api.errors[error.__class__.__name__]["code"]
                    )
                else:
                    code = api.errors[error.__class__.__name__]["code"]

                return {
                    "message": error.custom_message,
                    "status": api.errors[error.__class__.__name__]["status"],
                    "code": code,
                }, getattr(error, "code", 500)
            else:
                return flask_restfull_default_handle_error(error)
        except:
            return flask_restfull_default_handle_error(error)

    api.handle_error = webapi_default_error_handler

    boto3.setup_default_session(
        aws_access_key_id="dummy",  # ローカルといえども何かを送る必要あるので値は適当
        aws_secret_access_key="dummy",  # 同上
        region_name="us-east-1",
    )
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000")
    cli_dynamo = boto3.client("dynamodb", endpoint_url=endpoint_url)
    cli_streams = boto3.client("dynamodbstreams", endpoint_url=endpoint_url)
    # 最新のDynamoDB Streams ARN取得
    stream_arn = cli_dynamo.describe_table(TableName="event")["Table"][
        "LatestStreamArn"
    ]
    print(f"stream arn: {stream_arn}")

    # 取得したARNからストリームに関して取得
    shard_iters = {}

    shards = cli_streams.describe_stream(StreamArn=stream_arn)["StreamDescription"][
        "Shards"
    ]

    # 具体的なシャードイテレーター取得
    for shard in shards:
        shard_id = shard["ShardId"]
        shard_iters[shard_id] = cli_streams.get_shard_iterator(
            StreamArn=stream_arn,
            ShardId=shard_id,
            ShardIteratorType="LATEST",
        )["ShardIterator"]

        print(shard_iters[shard_id])

    while True:
        # if cli_streams.exceptions:
        #     continue
        # 開いているものがなかったら終了する
        if len(shard_iters) == 0:
            break

        # イテレーターごとに更新がないか読む
        for shard_id, cur_iter in [*shard_iters.items()]:
            # イテレーターが閉じられているのを確認
            if cur_iter is None:
                print(f"closed shard: {shard_id}")
                del shard_iters[shard_id]  # 現在のイテレーターをテーブルから削除
                continue
            try:
                records = cli_streams.get_records(ShardIterator=cur_iter)
            except Exception:
                continue

            # イテレーターを更新
            # 上で処理しているが `NextShardIterator` が None の場合はそのイテレーターは閉じられた
            next_iter = records.get("NextShardIterator")

            # 取得した次のイテレーターに変更がないならスキップ
            if next_iter == cur_iter:
                continue

            shard_iters[shard_id] = next_iter

            # レコードが取得できなかった場合はスキップ
            if len(records["Records"]) == 0:
                continue

            print(f"Lambda event data count: {len(records['Records'])}")
            print(records["Records"][0]["dynamodb"]["NewImage"])

            # AWS Lambda 呼び出し
            # lambda_handler(event=records, context=None)
    return app


app = create_app()
