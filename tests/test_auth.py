import pytest


def test_show_signup(client):
    rv = client.get('/signup')
    assert 'サインアップ' in rv.data.decode('utf-8')


def test_show_login(client):
    rv = client.get('/login')
    assert 'ログイン' in rv.data.decode('utf-8')


@pytest.mark.parametrize(('name', 'email', 'password', 'confirm', 'message'), (
    # 正常登録
    ('name1', 'email1@mail.com', 'pass', 'pass', '登録しました。'),
    # 名前チェック
    ('', 'email2@mail.com', 'pass', 'pass', '必須です'),
    ('0123456789'*8 + 'a', 'email3@mail.com', 'pass', 'pass', '80桁まで'),
    ('0123456789'*8, 'email4@mail.com', 'pass', 'pass', '登録しました。'),
    # メールチェック
    ('name5', '', 'pass', 'pass', '必須です'),
    ('name6', 'email6mail.com', 'pass', 'pass', '形式が違います'),
    ('name7', '0123456789'*11 + '@amail.coma', 'pass', 'pass', '120桁まで'),
    ('name8', '0123456789'*11 + '@amail.com', 'pass', 'pass', '登録しました。'),
    # パスワードチェック
    ('name9', 'email9@mail.com', '', 'pass', '必須です'),
    ('name10', 'email10@mail.com', '0123456789a'*3, 'pass', '30桁まで'),
    ('name11', 'email11@mail.com', '0123456789'*3, '0123456789'*3, '登録しました。'),
    ('name12', 'email12@mail.com', 'pass', 'passa', '一致していません'),
    # 再入力チェック
    ('name13', 'email13@mail.com', 'pass', '', '必須です'),
    # ユニークチェック
    ('name1', 'email14@mail.com', 'pass', 'pass', 'すでに使われています'),
    ('name15', 'email1@mail.com', 'pass', 'pass', 'すでに使われています'),
))
def test_validate_signup(client, name, email, password, confirm, message):
    rv = client.post(
        '/signup',
        data={'name': name, 'password': password, 'email': email,
              'password': password, 'confirm': confirm},
        follow_redirects=True
    )
    assert message in rv.data.decode('utf-8')


@pytest.mark.parametrize(('email', 'password', 'message'), (
    # 正常系
    ('email1@mail.com', 'pass', 'ログインしました'),
    # メールチェック
    ('', 'pass', '必須です'),
    ('0123456789'*11 + '@amail.coma', 'pass', '120桁まで'),
    ('email1mail.com', 'pass', '形式が違います'),
    # パスワード
    ('email1@mail.com', '', '必須です'),
    ('email1@mail.com', '0123456789a'*3, '30桁まで'),
    # 異常系
    ('email1x@mail.com', 'pass', 'メールアドレスかパスワードが違います'),
    ('email1@mail.com', 'passx', 'メールアドレスかパスワードが違います'),
))
def test_validate_login(client, email, password, message):
    rv = client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)
    assert message in rv.data.decode('utf-8')


def test_redirect_logout(client):
    rv = client.get('/logout', follow_redirects=True)
    assert 'ログインしてください' in rv.data.decode('utf-8')
