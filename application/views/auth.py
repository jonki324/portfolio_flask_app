from application.froms.signup import SignupForm
from flask import (Blueprint, current_app, render_template)

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth_view.route('/signup', methods=['GET', 'POST'])
def signup():
    current_app.logger.info('サインアップ処理開始')
    form = SignupForm()
    return render_template('signup.html', form=form)
