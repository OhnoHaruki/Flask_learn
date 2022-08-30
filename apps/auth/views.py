from flask import Blueprint, render_template

# Blueprintを使ってauthを生成する
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# indexエンドポイントの作成
@auth.route("/")
def index():
    return render_template("auth/index.html")
