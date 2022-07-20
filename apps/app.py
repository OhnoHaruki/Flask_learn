from flask import Flask


# create_app関数を使用する
def create_app():
    # Flaskインスタンスを作成
    app = Flask(__name__)

    # crudパッケージからviewsをインポートする
    from apps.crud import views as crud_views

    # register_blueprintsを使ってviewsのcrudアプリをアプリへ登録
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app
