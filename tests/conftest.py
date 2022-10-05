"""
conftest.py：テストを行うにあたり、さまざまなファイルなどを一斉にテストできるように処理を行うファイル

参考ページ：
p.269：conftest.pyの作成def app_dataの作成
p.273：セットアップ処理とクリーンアップ処理の追加

メモ：
yeild文とは：
    yeildとは関数を一時的に実行を停止できる機能を持つ機能。
    この機能を使うことで膨大な量の戻り値を小分けにして返す事ができる。
"""


import os
import shutil

import pytest
from apps.app import create_app, db
from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


# フィクスチャ関数の作成
@pytest.fixture
def fixture_app():
    # セットアップの処理
    # テスト用のコンフィグを使うために引数にtestingを指定する
    app = create_app("testing")

    # データベースを利用するための宣言をする
    app.app_context().push()

    # テスト用データベースのテーブルを作成する
    with app.app_context():
        db.create_all()

    # テスト用の画像アップデートディレクトリを作成する
    os.mkdir(app.config["UPLOAD_FOLDER"])

    # テストを実行する
    yield app

    # クリーンアップの処理
    # userテーブルのレコードを削除する
    User.query.delete()

    # user_imageテーブルのレコードを削除する
    UserImage.query.delete()

    # user_image_tagsテーブルのレコードを削除する
    UserImageTag.query.delete()

    # テスト用画像のディレクトリを削除する
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()


# flaskのテストクライアントを返すフィクスチャ関数を作成する
@pytest.fixture
def client(fixture_app):
    # flaskのテスト用クライアントを返す
    return fixture_app.test_client()
