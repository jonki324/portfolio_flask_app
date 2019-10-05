class Config(object):
    DEBUG = False
    TESTING = False
    LOG_FILE_NAME = 'application.log'
    LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_FILE_NAME = 'development.log'


class TestingConfig(Config):
    TESTING = True
    LOG_FILE_NAME = 'testing.log'
