# このファイルはVSCodeで開発するとき、Debug用の目的でFlaskを起動するのEntryファイルです
# 本番にはこのファイルを使われてない

from dotenv import load_dotenv

load_dotenv(".flaskenv")

if __name__ == '__main__':
    from src.app import app
    app.run(host='0.0.0.0', port=5000, debug=True)
