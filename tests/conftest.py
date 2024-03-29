import os
import tempfile

import pytest

from application import create_app
from application.models.database import create_db


@pytest.fixture(scope='module')
def app():
    app = create_app()

    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)

    # DB_USER = 'dbuser'
    # DB_PASS = 'dbpass'
    # DB_HOST = 'localhost'
    # DB_PORT = '5432'
    # DB_URI = 'postgresql+psycopg2://{}:{}@{}:{}/portfolio_flask_app'.format(DB_USER, DB_PASS,
    #                                                                         DB_HOST, DB_PORT)
    # app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

    with app.app_context():
        create_db(app)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
