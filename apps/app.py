from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# create_app関数を使用する
def create_app():
    # Flaskインスタンスを作成
    app = Flask(__name__)
    # アプリのコンフィグ設定
    # SQLalchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを設定する
    Migrate(app, db)
    # crudパッケージからviewsをインポートする
    from apps.crud import views as crud_views

    # register_blueprintsを使ってviewsのcrudをアプリへ登録
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app
