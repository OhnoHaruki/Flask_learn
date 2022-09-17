from pathlib import Path

basedir = Path(__file__).parent.parent

# BaseConfigクラスを作成


class BaseConfig:
    SECRET_KEY = "AFdcd142agaHKen28Jirn3J"
    WTF_CSRF_SECRET_KEY = "AGvkerij23j3fj3fj8rb"
    # 画像アップロード先にapps/imagesを指定する
    UPLOAD_FOLDER = str(Path(basedir, "apps", "images"))


# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
