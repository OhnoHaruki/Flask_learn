# dbをインポート
from apps.apps import db

# Userクラスをインポートする
from apps.crud.models import User
from flask import Blueprint, render_template

# Blueprintでcrudアプリを作成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# indexエンドポイントを作成し、index.htmlを返す
@crud.route("/")
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "コンソールログを確認してください"
