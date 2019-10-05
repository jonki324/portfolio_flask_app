import os
from flask import Flask, render_template


def create_app():
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

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
