from apps.app import db
from apps.crud.models import User
from apps.detector.models import UserImage
from flask import Blueprint, current_app, render_template, send_from_directory

# template_folderを指定する(staticは指定しない)
dt = Blueprint("detector", __name__, template_folder="templates")


# dtアプリケーションを使ってエンドポイントを作成する
@dt.route("/")  # 画像画面一覧
def index():
    # UserとUserImageをjoinして画像一覧を所得する
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )
    return render_template("detector/index.html")


@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
