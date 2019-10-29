import os

import pytest


def signup(client):
    data = {'user_id': 'user01', 'email': 'user01@email.com',
            'password': 'pass', 'confirm': 'pass'}
    client.post('/signup', data=data, follow_redirects=True)


def login(client):
    user = {'email': 'user01@email.com', 'password': 'pass'}
    client.post('/login', data=user, follow_redirects=True)


def test_show_post_add_not_login(client):
    rv = client.get('/post/add', follow_redirects=True)
    assert 'ログインしてください' in rv.data.decode('utf-8')


def test_show_post_upd_not_login(client):
    rv = client.get('/post/upd/1', follow_redirects=True)
    assert 'ログインしてください' in rv.data.decode('utf-8')


def test_show_post_rmv_not_login(client):
    rv = client.get('/post/rmv/1', follow_redirects=True)
    assert 'ログインしてください' in rv.data.decode('utf-8')


def test_show_post_add(client):
    signup(client)
    login(client)
    rv = client.get('/post/add', follow_redirects=True)
    assert '記事投稿' in rv.data.decode('utf-8')


@pytest.mark.parametrize(('title', 'body', 'image', 'is_img_saved', 'message'), (
    # タイトル
    ('0123456789'*10 + 'x', 'comment', 'test01.jpg', '', '100桁までです'),
    ('', 'comment', 'test01.jpg', '', '必須です'),
    # コメント
    ('title', '0123456789'*20 + 'x', 'test01.jpg', '', '200桁までです'),
    ('title', '', 'test01.jpg', '', '必須です'),
    # ピクチャ
    ('title', 'comment', 'test05.png', '', 'jpgファイルのみです'),
    ('title', 'comment', '', '', '必須です'),
))
def test_invalid_post_add(client, title, body, image, is_img_saved, message):
    login(client)
    file_path = os.path.join('./tests/assets', image)
    if not image:
        data = {'title': title, 'body': body, 'image': (b'', ''), 'is_img_saved': is_img_saved}
        rv = client.post('/post/add', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')
    else:
        with open(file_path, 'rb') as f:
            data = {'title': title, 'body': body, 'image': (f, f.name),
                    'is_img_saved': is_img_saved}
            rv = client.post('/post/add', data=data, follow_redirects=True,
                             content_type='multipart/form-data')
            assert message in rv.data.decode('utf-8')


@pytest.mark.parametrize(('title', 'body', 'image', 'is_img_saved', 'message'), (
    ('title01', 'comment01', 'test01.jpg', '', '投稿しました'),
))
def test_valid_post_add(client, title, body, image, is_img_saved, message):
    login(client)
    file_path = os.path.join('./tests/assets', image)
    with open(file_path, 'rb') as f:
        data = {'title': title, 'body': body, 'image': (f, f.name), 'is_img_saved': is_img_saved}
        rv = client.post('/post/add', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')


def test_show_post_upd(client):
    login(client)
    rv = client.get('/post/upd/1', follow_redirects=True)
    assert '記事投稿' in rv.data.decode('utf-8')


def test_show_post_upd_not_exist(client):
    login(client)
    rv = client.get('/post/upd/2', follow_redirects=True)
    assert '記事がありません' in rv.data.decode('utf-8')


@pytest.mark.parametrize(('title', 'body', 'image', 'is_img_saved', 'message'), (
    # タイトル
    ('0123456789'*10 + 'x', 'comment', 'test01.jpg', 'y', '100桁までです'),
    ('', 'comment', 'test01.jpg', 'y', '必須です'),
    # コメント
    ('title', '0123456789'*20 + 'x', 'test01.jpg', 'y', '200桁までです'),
    ('title', '', 'test01.jpg', 'y', '必須です'),
    # ピクチャ
    ('title', 'comment', 'test05.png', 'y', 'jpgファイルのみです'),
))
def test_invalid_post_upd(client, title, body, image, is_img_saved, message):
    login(client)
    file_path = os.path.join('./tests/assets', image)
    with open(file_path, 'rb') as f:
        data = {'title': title, 'body': body, 'image': (f, f.name), 'is_img_saved': is_img_saved}
        rv = client.post('/post/upd/1', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')


@pytest.mark.parametrize(('title', 'body', 'image', 'is_img_saved', 'message', 'upd'), (
    # タイトル
    ('title02', 'comment01', 'test01.jpg', 'y', '更新しました', 'title02'),
    # コメント
    ('title01', 'comment02', 'test01.jpg', 'y', '更新しました', 'comment02'),
    # ピクチャ
    ('title01', 'comment01', 'test02.jpg', 'y', '更新しました', '4AAQSkZJRgABAQAAAQABAAD'),
    ('title01', 'comment01', '', 'y', '更新しました', '4AAQSkZJRgABAQAAAQABAAD'),
))
def test_valid_post_upd(client, title, body, image, is_img_saved, message, upd):
    login(client)
    file_path = os.path.join('./tests/assets', image)
    if image:
        with open(file_path, 'rb') as f:
            data = {'title': title, 'body': body, 'image': (f, f.name),
                    'is_img_saved': is_img_saved}
            rv = client.post('/post/upd/1', data=data, follow_redirects=True,
                             content_type='multipart/form-data')
            assert message in rv.data.decode('utf-8')
            assert upd in rv.data.decode('utf-8')
    else:
        data = {'title': title, 'body': body, 'image': (b'', ''), 'is_img_saved': is_img_saved}
        rv = client.post('/post/upd/1', data=data, follow_redirects=True,
                         content_type='multipart/form-data')
        assert message in rv.data.decode('utf-8')
        assert upd in rv.data.decode('utf-8')


def test_show_post_rmv_get_method(client):
    login(client)
    rv = client.get('/post/rmv/1', follow_redirects=True)
    assert 'Blog' in rv.data.decode('utf-8')


def test_show_post_rmv_not_exist(client):
    login(client)
    rv = client.post('/post/upd/2', follow_redirects=True)
    assert '記事がありません' in rv.data.decode('utf-8')


def test_valid_post_rmv(client):
    login(client)
    rv = client.post('/post/rmv/1', follow_redirects=True)
    assert '削除しました' in rv.data.decode('utf-8')
    assert 'title01' not in rv.data.decode('utf-8')
