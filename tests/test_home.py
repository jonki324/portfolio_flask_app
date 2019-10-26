import os
import time


def signup(client):
    data = {'user_id': 'user01', 'email': 'user01@email.com',
            'password': 'pass', 'confirm': 'pass'}
    client.post('/signup', data=data, follow_redirects=True)


def login(client):
    user = {'email': 'user01@email.com', 'password': 'pass'}
    client.post('/login', data=user, follow_redirects=True)


def logout(client):
    client.get('/logout', follow_redirects=True)


def add_posts(client):
    signup(client)
    login(client)
    for i in range(1, 21):
        title = 'title{}'.format(i)
        body = 'body{}'.format(i)
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
        time.sleep(0.2)
    logout(client)


def test_setup(client):
    add_posts(client)


def test_show_home_not_login(client):
    rv = client.get('/', follow_redirects=True)
    assert 'login' in rv.data.decode('utf-8')
    assert 'logout' not in rv.data.decode('utf-8')
    assert 'MyBlog' not in rv.data.decode('utf-8')
    assert '記事一覧' not in rv.data.decode('utf-8')
    assert '投稿する' not in rv.data.decode('utf-8')
    assert 'onclick="addBookmarkPost' not in rv.data.decode('utf-8')


def test_show_home_login(client):
    login(client)
    rv = client.get('/', follow_redirects=True)
    assert 'login' not in rv.data.decode('utf-8')
    assert 'logout' in rv.data.decode('utf-8')
    assert 'MyBlog' in rv.data.decode('utf-8')
    assert '記事一覧' in rv.data.decode('utf-8')
    assert '投稿する' in rv.data.decode('utf-8')
    assert 'onclick="addBookmarkPost' in rv.data.decode('utf-8')


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
    rv = client.get('/', follow_redirects=True)
    assert 'title20' in rv.data.decode('utf-8')
    assert 'title3' not in rv.data.decode('utf-8')


def test_search_post_keyword(client):
    query = {
        'keyword': 'title3'
    }
    rv = client.get('/', query_string=query, follow_redirects=True)
    assert 'body3' in rv.data.decode('utf-8')
    assert 'body20' not in rv.data.decode('utf-8')


def test_search_post_page(client):
    query = {
        'page': 2
    }
    rv = client.get('/', query_string=query, follow_redirects=True)
    assert 'title3' in rv.data.decode('utf-8')
    assert 'title20' not in rv.data.decode('utf-8')
