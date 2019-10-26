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
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_SECRET_KEY = os.urandom(24)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024


class ProductionConfig(Config):
    pass


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
