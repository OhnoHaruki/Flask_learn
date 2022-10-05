"""
テストを行う。
ログイン時と未ログイン時の2通りで表示の確認を行う。

参考ページ：
p.275：画像一覧画面のテストを行う。未ログイン時とログイン時のコード作成
p.277：画像アップロード画面のテストを行う。
"""
from pathlib import Path

from apps.detector.models import UserImage
from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage


# 画像一覧画面
def test_index(client):  # 未ログイン時
    rv = client.get("/")
    assert "ログイン" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def signup(client, username, email, password):  # サインアップ
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)


def test_index_signup(client):  # サインアップの実行
    rv = signup(client, "admin", "flaskbook@example.com", "passwrord")
    assert "admin" in rv.data.decode()

    rv = client.get("/")
    assert "ログアウト" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


# 画像アップロード画面


def test_upload_no_auth(client):
    rv = client.get("/upload", follow_redirects=True)
    # 画像アップロード画面にはアクセスできない
    assert "アップロード" not in rv.data.decode()
    # ログイン画面へリダイレクトする
    assert "メールアドレス" in rv.data.decode()
    assert "パスワード" in rv.data.decode()


def test_upload_signup_get(client):
    signup(client, "admin", "flaskbook@example.com", "passwrord")
    rv = client.get("/upload")
    assert "アップロード" in rv.data.decode()


# 画像アップロードのバリデートエラー時
def upload_image(client, image_path):
    # 画像をアップロードする
    image = Path(get_root_path("tests"), image_path)

    test_file = (
        FileStorage(
            stream=open(image, "rb"),
            filename=Path(image_path).name,
            content_type="multipart/form-data",
        ),
    )

    data = dict(
        image=test_file,
    )
    return client.post("/upload", data=data, follow_redirects=True)


def test_upload_signup_post_validate(client):
    signup(client, "admin", "flaskbook@example.com", "passwrord")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    assert "サポートされていない画像形式です。" in rv.data.decode()


def test_upload_signup_post(client):
    signup(client, "admin", "flaskbook@example.com", "passwrord")
    rv = upload_image(client, "detector/testdata/test_invalid_image.jpg")
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


def test_detect_no_user_image(client):  # バリデートエラー
    signup(client, "admin", "flaskbook@example.com", "passwrord")
    upload_image(client, "detector/testdata/test_invalid_image.jpg")
    # 存在しないIDを指定する
    rv = client.post("/detect/notexistid", follow_redirects=True)
    assert "物体検知対象の画像が存在しません。" in rv.data.decode()


def test_detect(client):  # 物体検知成功時
    signup(client, "admin", "flaskbook@example.com", "passwrord")
    # 画像のアップロード
    upload_image(client, "detector/testdata/test_invalid_image.jpg")
    user_image = UserImage.query.first()

    # 物体検知を実行
    rv = client.post(f"/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()


def test_delete(client):  # 画像削除機能
    signup(client, "admin", "flaskbook@example.com", "passwrord")
    upload_image(client, "detector/testdata/test_invalid_image.jpg")

    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f"/images/delete/{user_image.id}", follow_redirects=True)
    assert image_path not in rv.data.decode()
