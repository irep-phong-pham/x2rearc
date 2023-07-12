# Irep WebAPI フレームワーク

## 概要

WebAPI は Python の Flask ベースのフレームワークです。3 つレイヤーの Controller & Service& Dao のアーキテクチャーで構築されている。

- Environment: 基本は Docker 使う
- 言語: python
- Dependencies 管理: Pipfile で管理
- Framework: Flask
- WebServer: nginx & uwsgi

## 開発

ローカルで開発するとき、2 つのモードで開発できる

- ① Docker で開発する: Docker を使うと、本番と同じ環境で開発できる
- ② Docker 使わないで開発する: VSCode で開発するとき、Docker を使わないで Debug しやすい。ただ、Debug 終わったらリリース前に、① のモードでもう 1 回テストした方が良い

今回のサンプルで、Todo アプリの WebAPI を構築する

## Docker で開発する

docker-compose を使って、開発する。
データベースは Mysql を使って、Docker で Mysql を起動する。

docker compose でビルドする

### Docker ビルド

```sh
# User ID & Group IDを環境変数で設定
export UID=$(id -u)
export GID=$(id -g)
# ビルド
docker-compose build
```

### Mysql 初期化

Mysql を docker-compose で起動する前に、Mysql 用のデータ保存ディレクトリ・ルートのパスワード設定を先にやった方が良い。設定のステップは以下となります。
Refs: https://hub.docker.com/_/mysql

#### ステップ 1: Mysql 用のデータ保存ディレクトリ作成

```sh
cd <project-dir>
mkdir -p data
```

#### ステップ 2: Mysql の Docker を起動して、ルートのパスワード設定する

```sh
docker-compose run -e MYSQL_ROOT_PASSWORD=<ルートのパスワード> db
# 例: docker-compose run -e MYSQL_ROOT_PASSWORD=root db
```

- `MYSQL_ROOT_PASSWORD`の環境変数にルートのパスワードを入力してください
  上記のコマンドを実行してから、ログが出力されるので Mysql 接続ができたまで待ってください

- 以下のサンプルのログです。「ready for connections」が出たら、Mysql 接続ができたということです

```sh
# 省略された。。。
# 2021-01-02T07:57:26.577318Z 4 [System] [MY-013381] [Server] Server upgrade from '80021' to '80022' completed.
# 2021-01-02T07:57:26.643406Z 0 [System] [MY-010229] [Server] Starting XA crash recovery...
# 2021-01-02T07:57:26.655879Z 0 [System] [MY-010232] [Server] XA crash recovery finished.
# 2021-01-02T07:58:04.675840Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
# 2021-01-02T07:58:04.676657Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
# 2021-01-02T07:58:04.694859Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
# 2021-01-02T07:58:04.718454Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.22'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```

#### ステップ 3: Mysql の Docker コンテナに入って、データベースの初期化

- 以下のコマンドで動いている全てコンテナをリストアップする

```sh
docker ps
# 結果の例:
# CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS                      NAMES
# a5958ac71b84        mysql                          "docker-entrypoint.s…"   7 minutes ago       Up 7 minutes        3306/tcp, 33060/tcp        webapi-fw_db_run_7be43268e91b
```

- Mysql のコンテナ ID をコピーして、以下のコマンドでコンテナの中に入ってください

```sh
docker exec -it　<container ID> bash
# 例: docker exec -it a5958ac71b84 bash
```

- DDL を実行して、TODO データベースを初期化する

```sh
mysql -h localhost -u root -p < /app/src/_ddl/ddl.sql
```

- 初期化のデータベースを確認する

```sh
mysql -h localhost -u root -p
```

```sql
mysql > show databases;
mysql > use test_database;
mysql > show tables;
mysql > select * from M_USERS;
mysql > select * from T_TASKS;
mysql > exit;
```

- データベースが初期化できたら、mysql の docker コンテナをストップする

```sh
docker rm -f <container-id>
# 例: docker rm -f a5958ac71b84
```

### Docker 起動して＆API テスト

#### Docker 起動

```sh
docker-compose up
```

#### API テスト

```sh
# ヘルシAPIのテスト
curl -X GET localhost:5000/healthy

# 存在するタスクの詳細のテスト
curl -X GET localhost:5000/tasks
curl -X GET localhost:5000/my-tasks
curl -X GET localhost:5000/task/1
curl -X GET localhost:5000/task/2
curl -X GET localhost:5000/task/3
curl -X GET localhost:5000/task/4

# get task that do not exists
curl -X GET localhost:5000/task/100

# create new task
curl -X POST -H "Content-Type: application/json" localhost:5000/task -d '{"title":"new_task", "description": "New Task"}'
```

## Docker 使わないで、VSCode で Debug

### VSCode インストール

こちらを参考しながらインストールしてください: https://code.visualstudio.com/download
もしくは、アイレップの`Self Service`からインストールしてください

### Pipenv インストール

こちらを参考してインストールしてください: https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv

### Pip Packages インストール

```sh
pipenv install --dev
```

### Pipenv の仮装環境の Python Path を確認しコピーする、VSCode 設定を変える

```sh
# python pathを確認して、
pipenv shell
which python
# 例: /Users/manh_nguyen/.local/share/virtualenvs/webapi-fw-6uvQav4N/bin/python

# copy settings.json.example to settings.json
cp  .vscode/settings.json.example .vscode/settings.json
```

### Background モードで mysql docker を起動する

- Run mysql docker

```sh
docker-compose run -d -p 3306:3306 db
```

- (`mysqlshell`)[https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html] で mysql 接続をチェックする

```sh
mysqlsh --sql --uri root@localhost:3306
```

```sql
show databases;
use test_database;
select * from M_USERS;
select * from T_TASKS;
```

### Debug with VSCode

- From Sidebar of VScode, click on debug Icon & select `Python: Flask IREPFW` and Run
- Set breakpoint for debug...

## 単体テスト

### Run Test

- docker-compose でアプリ起動

```sh
docker-compose up
docker-compose ps
# a91edcfc191a        mysql                          "docker-entrypoint.s…"   11 seconds ago      Up 10 seconds       0.0.0.0:3306->3306/tcp, 33060/tcp         webapi-fw_db_1
# c2d038b515e5        webapi-fw_app                  "/entrypoint.sh /sta…"   About an hour ago   Up 10 seconds       80/tcp, 443/tcp, 0.0.0.0:5000->5000/tcp   webapi-fw_app_1

```

- webapi の docker コンテナに入る

```sh
docker exec -it <container id> bash
#  docker exec -it c2d038b515e5 bash
```

- pipenv を起動する

```sh
pipenv shell
```

- Run test

```sh
pytest
```

### 単体テスト開発

- `tests/`フォルダーの中にテストを書いてください。
- テストケースの書き方は基本`pytest`ライブラを使うので、書き方はこちらを参考してください
  - Qiita: https://qiita.com/sasaki77/items/97c90ae272373d78b422
  - pytest Official: https://docs.pytest.org/en/stable/contents.html
- 少なくとも、`services`のテストを行ってください。このフレームワークには、`services/`に`task_services.py`というサービスがあるので、`tests/services/`の中に`test_task_service.py`を作って、テストケースを作成しました。
- 単体テストには、基本データベースを使わない。全部 DAO の部分をモックする。詳細は`tests/services/test_task_service.py`と`tests/mock`をチェックしてください

# Appendix

## 環境変数

- 以下が環境変数のサンプルとなる

```sh
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@<db hostname>:<db port>/<db name>
TZ='Asia/Tokyo'
DEBUG=True
BYPASS_AUTH=True
```

- `SQLALCHEMY_DATABASE_URI`: データベースの接続 URI
- `TZ`: Timezone 設定
- `DEBUG`: True|False で設定可能。デーバグしたいとき、True で設定してください
- `BYPASS_AUTH`: True|False で設定可能。True で設定することで、実際の CognitoToken から user_id を抽出しないで、mock の user_id で API テストできる。詳細は`controllers/base_controller.py`を確認してください
