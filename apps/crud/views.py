# dbをインポート
from apps.app import db
from apps.crud.forms import UserForm

# Userクラスをインポートする
from apps.crud.models import User
from flask import Blueprint, redirect, render_template, url_for

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


@crud.route("/Users/new", methods=["GET", "POST"])
def create_user():
    # UserFormをインスタンス化する
    form = UserForm()
    # フォームの値をバリデートする
    if form.validate_on_submit():
        # ユーザを作成する
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # ユーザを追加してコミットする
        db.session.add(user)
        db.session.commit()
        # ユーザ一案画面にリダイレクトする
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)
