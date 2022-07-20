# 仮想環境('venv':venv)で作成
import logging
import os

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)

# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "5jaojJOWJ97joeoHOMoho245iH"
# ログレベルの設定
app.logger.setLevel(logging.DEBUG)
app.logger.critical("fetal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")
# リダイレクトを中断しないようにする
app.config["DEBUG_TP_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtensionにアプリケーションをセット
toolbar = DebugToolbarExtension(app)

# Mailクラスのコンフィグを追加する
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_POST"] = os.environ.get("MAIL_POST")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail拡張を登録する
mail = Mail(app)


@app.route("/")
def index():
    return "Hello, Flask!!"


@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


with app.test_request_context():
    print(url_for("index"))  # /
    print(url_for("hello-endpoint", name="world"))  # /hello/world
    print(url_for("show_name", name="haruki", page="1"))  # /name/haruki?page=haruki

# アプリケーションコンテキストを所得してスタックへpushする
ctx = app.app_context()
ctx.push()

# current_appにアクセスが可能になる
print(current_app.name)

# グローバルなテンポラリ領域に値を設定する
g.connection = "connection"
print(g.connection)

with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))


@app.route("/contact")  # お問い合わせフォーム
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])  # お問い合わせフォームの処理とお問合せ完了画面を返す
def contact_complete():
    if request.method == "POST":  # リクエストされたメソッドのチェック
        # form属性を使ってフォームの値を所得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True

        if not username:
            flash("ユーザ名は必須です。")
            is_valid = False
        if not email:
            flash("メールアドレスは必須です。")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください。")
            is_valid = False

        if not description:
            flash("良い合わせ内容は必須です。")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        # メールを送る
        send_email(
            email,
            "お問合せありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )
        # contactエンドポイントへリダイレクトする
        flash("お問合せありがとうございました。")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(
        subject,
        recipients=[to],
        body=render_template(template + ".txt", **kwargs),
        html=render_template(template + ".html", **kwargs),
    )
    mail.send(msg)
