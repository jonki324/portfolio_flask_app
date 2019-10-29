import os
from pathlib import Path


class Config(object):
    DEBUG = False
    TESTING = False
    LOG_DIR = str(Path(__file__).resolve().parents[1] / 'log')
    LOG_FILE_NAME = 'application.log'
    LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATIONS_DIR = str(Path(__file__).parent / 'migrations')
    SECRET_KEY = os.environ.get('SECRET_KEY', default=os.urandom(24))
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', default=os.urandom(24))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024


class ProductionConfig(Config):
    DB_USER = 'dbuser'
    DB_PASS = 'dbpass'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_URI = 'postgresql+psycopg2://{}:{}@{}:{}/portfolio_flask_app'.format(DB_USER, DB_PASS,
                                                                            DB_HOST, DB_PORT)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', default=DB_URI)


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_FILE_NAME = 'development.log'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(str(Path(__file__)
                                                        .resolve().parents[1] / 'development.db'))


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOG_FILE_NAME = 'testing.log'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(str(Path(__file__)
                                                        .resolve().parents[1] / 'testing.db'))
    WTF_CSRF_ENABLED = False
