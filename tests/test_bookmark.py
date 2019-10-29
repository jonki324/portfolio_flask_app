import os
import time


def signup(client):
    data1 = {'user_id': 'user01', 'email': 'user01@email1.com', 'password': 'pass',
             'confirm': 'pass'}
    data2 = {'user_id': 'user02', 'email': 'user02@email2.com', 'password': 'pass',
             'confirm': 'pass'}
    client.post('/signup', data=data1, follow_redirects=True)
    time.sleep(0.2)
    client.post('/signup', data=data2, follow_redirects=True)


def login(client):
    user = {'email': 'user01@email1.com', 'password': 'pass'}
    client.post('/login', data=user, follow_redirects=True)


def login_user02(client):
    user = {'email': 'user02@email2.com', 'password': 'pass'}
    client.post('/login', data=user, follow_redirects=True)


def logout(client):
    client.get('/logout', follow_redirects=True)


def add_posts_user01(client):
    login(client)
    for i in range(2):
        title = 'u01_title{}'.format(i)
        body = 'u01_body{}'.format(i)
        image = 'test03.jpg'
        file_path = os.path.join('./tests/assets', image)
        is_img_saved = ''
        with open(file_path, 'rb') as f:
            data = {
                'title': title,
                'body': body,
                'image': (f, f.name),
                'is_img_saved': is_img_saved
            }
            client.post('/post/add', data=data, follow_redirects=True,
                        content_type='multipart/form-data')
        time.sleep(1)
    logout(client)


def add_posts_user02(client):
    login_user02(client)
    for i in range(2):
        title = 'u02_title{}'.format(i)
        body = 'u02_body{}'.format(i)
        image = 'test04.jpg'
        file_path = os.path.join('./tests/assets', image)
        is_img_saved = ''
        with open(file_path, 'rb') as f:
            data = {
                'title': title,
                'body': body,
                'image': (f, f.name),
                'is_img_saved': is_img_saved
            }
            client.post('/post/add', data=data, follow_redirects=True,
                        content_type='multipart/form-data')
        time.sleep(1)
    logout(client)


def test_setup(client):
    signup(client)
    add_posts_user01(client)
    add_posts_user02(client)


def test_add_bookmark_post(client):
    login(client)
    rv = client.post('/bookmark/post/add', data={'post_id': 1}, follow_redirects=True)
    assert '登録しました' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 1' in rv.data.decode('unicode_escape')
    assert '"del_flg": true' in rv.data.decode('unicode_escape')


def test_add_duplicate_bookmark_post(client):
    login(client)
    rv = client.post('/bookmark/post/add', data={'post_id': 1}, follow_redirects=True)
    assert '登録済みです' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 1' in rv.data.decode('unicode_escape')
    assert '"del_flg": true' in rv.data.decode('unicode_escape')


def test_rmv_bookmark_post(client):
    login(client)
    rv = client.post('/bookmark/post/rmv', data={'post_id': 1}, follow_redirects=True)
    assert '解除しました' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 0' in rv.data.decode('unicode_escape')
    assert '"del_flg": false' in rv.data.decode('unicode_escape')


def test_rmv_duplicate_bookmark_post(client):
    login(client)
    rv = client.post('/bookmark/post/rmv', data={'post_id': 1}, follow_redirects=True)
    assert '解除済みです' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 0' in rv.data.decode('unicode_escape')
    assert '"del_flg": false' in rv.data.decode('unicode_escape')


def test_add_bookmark_user(client):
    login(client)
    rv = client.post('/bookmark/user/add', data={'user_id': 'user02'}, follow_redirects=True)
    assert '登録しました' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 1' in rv.data.decode('unicode_escape')
    assert '"del_flg": true' in rv.data.decode('unicode_escape')


def test_add_duplicate_bookmark_user(client):
    login(client)
    rv = client.post('/bookmark/user/add', data={'user_id': 'user02'}, follow_redirects=True)
    assert '登録済みです' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 1' in rv.data.decode('unicode_escape')
    assert '"del_flg": true' in rv.data.decode('unicode_escape')


def test_rmv_bookmark_user(client):
    login(client)
    rv = client.post('/bookmark/user/rmv', data={'user_id': 'user02'}, follow_redirects=True)
    assert '解除しました' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 0' in rv.data.decode('unicode_escape')
    assert '"del_flg": false' in rv.data.decode('unicode_escape')


def test_rmv_duplicate_bookmark_user(client):
    login(client)
    rv = client.post('/bookmark/user/rmv', data={'user_id': 'user02'}, follow_redirects=True)
    assert '解除済みです' in rv.data.decode('unicode_escape')
    assert '"bookmark_count": 0' in rv.data.decode('unicode_escape')
    assert '"del_flg": false' in rv.data.decode('unicode_escape')
