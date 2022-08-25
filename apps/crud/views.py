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


@crud.route("/users")
def users():
    # ユーザの一覧を所得
    users = User.query.all()
    return render_template("crud/index.html", users=users)


# methodsにGETとPOSTを指定する
@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    # Userモデルを利用してユーザをを所得する
    user = User.query.filter_by(id=user_id).first()

    # formからサブミットされた場合はユーザを更新しユーザの一覧画面へリダイレクトする
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GETの場合はHTMLを返す
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/usrs/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
