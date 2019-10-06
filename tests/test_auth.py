import os
import tempfile

import pytest

from application import create_app
from application.models.database import create_db


@pytest.fixture(scope='module')
def client():
    app = create_app()

    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)

    client = app.test_client()

    with app.app_context():
        create_db(app)

    yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_show_signup(client):
    rv = client.get('/signup')
    assert 'サインアップ' in rv.data.decode('utf-8')


def test_show_login(client):
    rv = client.get('/login')
    assert 'ログイン' in rv.data.decode('utf-8')
