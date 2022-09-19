"""
このアプリの基本となるファイル

参考ページと参考内容:
p.86：app.pyの作成、create_app関数を作成してflaskインスタンスを生成する。Blueprintの説明~p.90まで
p.97：SQLAlchemyのセットアップ
p.104：SQLログを出力させる。SQLAlchemyを使った基本的なデータ操作
p.113：CSRF対策を施す(p.56参照)
p.136：コンフィグオブジェクトの読み込み
p.144：Blueprintで認証機能を登録する


メモ：
create_app関数はFlaskアプリを生成する関数。これがあることで簡単に開発環境やステージング(テスト)環境、本番環境など、環境を切り替える事ができる。これにより、テストしやすくなる。

Blueprintとは：Blueprintとはアプリを分割するためのFlaskの機能である。コレを使うことでアプリが大規模になっても簡潔な状態を保つ事ができ、保守性が向上する。

flask-migrate：コード情報をもとにデータベースのテーブルの作成やカラム変更などを行うための機能です。コードの情報をもとにSQLが発行され、SQL情報をファイルに保持するため、継続的にデータベースの更新や更新前の状態に戻すロールバックが可能になる。

CSRF：webアプリの脆弱性のうちの一つ。p.56ページを参照。

"""
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

    # これから作成するdetectorパッケージからviewsをimportする
    from apps.detector import views as dt_views

    # register_blueprintを使い、viewsのdtをアプリへ登録する
    app.register_blueprint(dt_views.dt)

    return app
