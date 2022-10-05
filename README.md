# Flask_learn
## このリポジトリの基本情報
Flaskを学習する際のファイルをgithubで管理するためのリポジトリ  

## 各ファイルまとめ
### appsディレクトリ
appsディレクトリはこのアプリの機能や見た目などのアプリの内部のほとんどを作成する  

app.py:アプリの最も基本となるファイル。アプリの設定などを行なっている。  

config.py:sqlや物体検知に関する設定を行なっている。  

### apps/authディレクトリ
このディレクトリはユーザのログインなどの機能を設定する  

forms.py:サインアップフォームの機能を設定する  
views.py:サインアップやログイン、ログアウトなどのユーザ情報系の見え方を作成する  


### apps/detectorディレクトリ
このディレクトリは物体検知アプリの各機能を設定する  

init.py:modelのインポート  
form.py:画像アップロード画面のフォームクラスを作成する  
models.py:ログインしたユーザが画像をアップロードした際に画像URLを保存するためのモデルを作成(SQLiteを用いたデータベースの作成)  
views.py:物体検知アプリケーションの見え方を作成するファイル  

### testsディレクトリ
これはアプリのテストを行うための設定などを行うためのディレクトリ

conftest.py:テストを行うにあたり、さまざまなファイルなどを一斉にテストできるように設定する  
test_sample.py:pytestを使用するにあたりチュートリアル的に作成したファイル  

### tests/detector
test_views.py:テストを行う際の機能を設定する。ログイン時と未ログイン時の二通りで設定する。  


### tests/detector/testdata
アプリのテストを行う際にこのtestdataに入っている画像やテキストファイルを参照してテストを行う。  

### 今回の研究室の内容と異なるため、スキップした部分
・第９章：検索機能を作る：p.244~p.251  
・第10章：カスタムエラー画面を作成する：p.254~p.260  


## 参考文献
参考書籍：Python FlaskによるWebアプリ開発入門 物体検知アプリ&機械学習APIの作り方(著：佐藤 昌基、平田 哲也、寺田 学、2022/1/24)  