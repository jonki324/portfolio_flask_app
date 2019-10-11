import logging
import logging.handlers
import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from application.models.database import db
from application.models.user import User
from application.views.auth import auth_view
from application.views.profile import profile_view
from application.views.blog import blog_view


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

    from application.models.blog_post import BlogPost
    from application.models.bookmark_post import BookmarkPost
    from application.models.profile import Profile

    # ログインセッション管理設定
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_view.login'
    login_manager.login_message = 'ログインしてください'
    login_manager.login_message_category = 'danger'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    # view登録
    app.register_blueprint(auth_view)
    app.register_blueprint(profile_view)
    app.register_blueprint(blog_view)

    @app.route('/')
    def index():
        app.logger.info('index処理開始')
        return render_template('index.html')

    return app
