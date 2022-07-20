from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemyをインスタンス化する
db = SQLAlchemy()


# create_app関数を使用する
def create_app():
    # Flaskインスタンスを作成
    app = Flask(__name__)
    # アプリのコンフィグ設定
    app.config.from_mapping(
        SECRET_KEY="AFdcd142agaHKen28Jirn3J",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLをコンソールログに出力する設定
        SQLALCHEMY_ECHO=True,
    )
    # SQLalchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを設定する
    Migrate(app, db)
    # crudパッケージからviewsをインポートする
    from apps.crud import views as crud_views

    # register_blueprintsを使ってviewsのcrudをアプリへ登録
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app
