# portfolio_flask_app
FlaskによるポートフォーリオWEBアプリケーション

## どんなアプリ？
Twitter、Instagram、はてなブックマークのようなブログアプリです。

[https://still-crag-30537.herokuapp.com/](https://still-crag-30537.herokuapp.com/)

## 開発フロー
GitHub上でのチーム開発を想定し、下記の工程で作業しました。
1. 開発する機能毎にissueを立てる
1. 開発用ブランチを切る
1. 作業完了後、masterブランチに対しプルリクエストを作成
1. 確認後、masterブランチにマージし、工程1へを繰り返す

## 工夫した点
- pipenvで仮想環境を管理
- flake8、autopep8を用いてコーディング規約遵守
- データベースマイグレーション機能追加による開発効率向上
- pytestを用いた自動テスト実施
- ORMを用いたデータベース操作
- その他各種Flaskプラグインを用いた開発効率の向上

## ローカル環境構築方法
```bash
# ソースコードをクローン
$ git clone https://github.com/jonki324/portfolio_flask_app.git

# プロジェクトフォルダに移動
$ cd portfolio_flask_app

# 仮想環境作成
$ pipenv sync --dev

# データベース初期化
$ pipenv run migrate

# アプリ起動
$ pipenv run start
```
