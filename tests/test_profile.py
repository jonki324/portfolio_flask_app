import os

import pytest


def signup(client):
    data = {'user_id': 'user01', 'email': 'user01@email.com',
            'password': 'pass', 'confirm': 'pass'}
    client.post('/signup', data=data, follow_redirects=True)


def login(client):
    user = {'email': 'user01@email.com', 'password': 'pass'}
    client.post('/login', data=user, follow_redirects=True)


def test_show_profile_not_login(client):
    rv = client.get('/profile', follow_redirects=True)
    assert 'ログインしてください' in rv.data.decode('utf-8')


def test_show_profile(client):
    signup(client)
    login(client)
    rv = client.get('/profile', follow_redirects=True)
    assert 'プロフィール' in rv.data.decode('utf-8')


@pytest.mark.parametrize(('nickname', 'comment', 'icon', 'icon_del', 'message'), (
    # ニックネーム
    ('0123456789'*8 + 'x', 'comment', 'test01.jpg', '', '80桁までです'),
    # コメント
    ('nickname', '0123456789'*20 + 'x', 'test01.jpg', '', '200桁までです'),
    # アイコン
    ('nickname', 'comment', 'test05.png', '', 'jpgファイルのみです'),
))
def test_invalid_profile(client, nickname, comment, icon, icon_del, message):
    login(client)
    file_path = os.path.join('./tests/assets', icon)
    with open(file_path, 'rb') as f:
        data = {'nickname': nickname, 'comment': comment, 'icon': (f, f.name),
                'icon_del': icon_del}
        rv = client.post('/profile', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')


@pytest.mark.parametrize(('nickname', 'comment', 'icon', 'icon_del', 'message'), (
    # ニックネーム
    ('nickname', 'comment', 'test01.jpg', '', 'プロフィールを更新しました'),
    ('', 'comment', 'test01.jpg', '', 'プロフィールを更新しました'),
    # コメント
    ('nickname', 'comment', 'test01.jpg', '', 'プロフィールを更新しました'),
    ('nickname', '', 'test01.jpg', '', 'プロフィールを更新しました'),
))
def test_valid_profile(client, nickname, comment, icon, icon_del, message):
    login(client)
    file_path = os.path.join('./tests/assets', icon)
    with open(file_path, 'rb') as f:
        data = {'nickname': nickname, 'comment': comment, 'icon': (f, f.name),
                'icon_del': icon_del}
        rv = client.post('/profile', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')


@pytest.mark.parametrize(('nickname', 'comment', 'icon', 'icon_del', 'message'), (
    # アイコン
    ('nickname', 'comment', 'test01.jpg', '', 'プロフィールを更新しました'),
    ('nickname', 'comment', '', 'y', 'プロフィールを更新しました'),
    ('nickname', 'comment', 'test01.jpg', '', 'プロフィールを更新しました'),
    ('nickname', 'comment', 'test02.jpg', 'y', 'プロフィールを更新しました'),
))
def test_valid_profile_icon(client, nickname, comment, icon, icon_del, message):
    login(client)
    if icon != '':
        file_path = os.path.join('./tests/assets', icon)
        with open(file_path, 'rb') as f:
            data = {'nickname': nickname, 'comment': comment, 'icon': (f, f.name),
                    'icon_del': icon_del}
            rv = client.post('/profile', data=data, follow_redirects=True,
                             content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')
    else:
        data = {'nickname': nickname, 'comment': comment, 'icon': (b'', ''), 'icon_del': icon_del}
        rv = client.post('/profile', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')
