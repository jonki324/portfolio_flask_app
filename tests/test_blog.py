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
    for i in range(10):
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
    for i in range(3):
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
        time.sleep(0.5)
    logout(client)


def test_setup(client):
    signup(client)
    add_posts_user01(client)
    add_posts_user02(client)


def test_show_blog_not_login(client):
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'プロフィール設定' not in rv.data.decode('utf-8')


def test_show_blog_login(client):
    login(client)
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'プロフィール設定' in rv.data.decode('utf-8')


def test_invalid_search_post(client):
    query = {
        'keyword': '0123456789' * 20 + 'x'
    }
    rv = client.get('/', query_string=query, follow_redirects=True)
    assert '200桁までです' in rv.data.decode('utf-8')


def test_valid_search_post(client):
    query = {
        'keyword': '0123456789'*20
    }
    rv = client.get('/', query_string=query, follow_redirects=True)
    assert '200桁までです' not in rv.data.decode('utf-8')


def test_search_post_default(client):
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'u01_title9' in rv.data.decode('utf-8')
    assert 'u01_title0' not in rv.data.decode('utf-8')
    assert 'u02' not in rv.data.decode('utf-8')


def test_search_post_keyword(client):
    query = {
        'keyword': 'title0'
    }
    rv = client.get('/blog/user01', query_string=query, follow_redirects=True)
    assert 'u01_body0' in rv.data.decode('utf-8')
    assert 'u01_body9' not in rv.data.decode('utf-8')
    assert 'u02' not in rv.data.decode('utf-8')


def test_search_post_page(client):
    query = {
        'page': 2
    }
    rv = client.get('/blog/user01', query_string=query, follow_redirects=True)
    assert 'title0' in rv.data.decode('utf-8')
    assert 'title9' not in rv.data.decode('utf-8')
    assert 'u02' not in rv.data.decode('utf-8')


def test_edit_post(client):
    login(client)
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'fas fa-trash-alt' in rv.data.decode('utf-8')
    rv = client.get('/blog/user02', follow_redirects=True)
    assert 'fas fa-trash-alt' not in rv.data.decode('utf-8')


def test_bookmark_user_login(client):
    login(client)
    rv = client.get('/blog/user02', follow_redirects=True)
    assert 'addBookmarkUser' in rv.data.decode('utf-8')
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'addBookmarkUser' not in rv.data.decode('utf-8')


def test_bookmark_user_logout(client):
    rv = client.get('/blog/user02', follow_redirects=True)
    assert 'addBookmarkUser' not in rv.data.decode('utf-8')
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'addBookmarkUser' not in rv.data.decode('utf-8')


def test_bookmark_post_login(client):
    login(client)
    rv = client.get('/blog/user02', follow_redirects=True)
    assert 'addBookmarkPost' in rv.data.decode('utf-8')
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'addBookmarkPost' in rv.data.decode('utf-8')


def test_bookmark_post_logout(client):
    rv = client.get('/blog/user02', follow_redirects=True)
    assert 'addBookmarkPost' not in rv.data.decode('utf-8')
    rv = client.get('/blog/user01', follow_redirects=True)
    assert 'addBookmarkPost' not in rv.data.decode('utf-8')
