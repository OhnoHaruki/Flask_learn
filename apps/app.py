from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

# SQLAlchemyをインスタンス化する
db = SQLAlchemy()

csrf = CSRFProtect()

# LoginManagerをインスタンス化
login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定する
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを指定する
# ここでは何も表示しないように空を指定
login_manager.login_message = ""


# create_app関数を使用する
def create_app(config_key):
    # Flaskインスタンスを作成
    app = Flask(__name__)
    # config_keyにマッチする環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])
    # アプリのコンフィグ設定
    app.config.from_mapping(
        SECRET_KEY="AFdcd142agaHKen28Jirn3J",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLをコンソールログに出力する設定
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="adaJIn153iAHoti497ragjoH",
    )

    csrf.init_app(app)
    # SQLalchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを設定する
    Migrate(app, db)

    # login_managerをアプリケーションと連携する
    login_manager.init_app(app)

    # crudパッケージからviewsをインポートする
    from apps.crud import views as crud_views

    # register_blueprintsを使ってviewsのcrudをアプリへ登録
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # authパッケージからviewsをimportする
    from apps.auth import views as auth_views

    # register_blueprintを使ってviewsのauthをアプリへ登録する
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app
