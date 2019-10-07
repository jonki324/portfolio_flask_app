from application.froms.signup import SignupForm
from application.froms.login import LoginForm
from application.models.user import User, db
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('ログイン処理開始')
    form = LoginForm()
    return render_template('login.html', form=form)


@auth_view.route('/signup', methods=['GET', 'POST'])
def signup():
    current_app.logger.info('サインアップ処理開始')
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('ユーザー登録処理開始')
        user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('登録しました。ログインしてください。', 'success')
        return redirect(url_for('auth_view.login'))

    return render_template('signup.html', form=form)
