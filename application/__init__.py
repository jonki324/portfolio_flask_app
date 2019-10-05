import logging
import logging.handlers
import os
from flask import Flask, render_template
from flask_migrate import Migrate
from application.models.database import db


def create_app():
    # アプリケーションの設定
    app = Flask(__name__, instance_relative_config=True)

    configs = {
        'production': 'ProductionConfig',
        'development': 'DevelopmentConfig',
        'testing': 'TestingConfig'
    }
    flask_env = os.environ.get('FLASK_ENV', default='production')
    app.config.from_object('application.config.{}'.format(configs[flask_env]))
    app.config.from_pyfile('application.cfg', silent=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # ロガー設定
    os.makedirs(app.config['LOG_DIR'], exist_ok=True)
    log_file = os.path.join(app.config['LOG_DIR'], app.config['LOG_FILE_NAME'])
    handler = logging.handlers.RotatingFileHandler(log_file, "a+",
                                                   maxBytes=3000,
                                                   backupCount=5)
    handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    app.logger.addHandler(handler)

    # データベース設定
    db.init_app(app)

    # データベースマイグレーション設定
    Migrate(app, db, directory=app.config['MIGRATIONS_DIR'])

    @app.route('/')
    def index():
        app.logger.info('index処理開始')
        return render_template('index.html')

    return app
