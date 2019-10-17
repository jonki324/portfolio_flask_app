from application.forms.signup import SignupForm
from application.forms.login import LoginForm
from application.models.user import User, db
from application.models.profile import Profile
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_login import login_user, logout_user, login_required

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('ログイン処理開始')
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('ログイン認証処理開始')
        user, authenticated = User.auth(db.session.query, form.email.data, form.password.data)
        if authenticated:
            current_app.logger.info('ログインユーザー: {}'.format(user))
            login_user(user)
            flash('ログインしました。', 'success')
            return redirect(url_for('home_view.index'))

        flash('メールアドレスかパスワードが違います', 'danger')

    return render_template('login.html', form=form)


@auth_view.route('/logout')
@login_required
def logout():
    current_app.logger.info('ログアウト処理開始')
    logout_user()
    flash('ログアウトしました。', 'success')
    return redirect(url_for('auth_view.login'))


@auth_view.route('/signup', methods=['GET', 'POST'])
def signup():
    current_app.logger.info('サインアップ処理開始')
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('ユーザー登録処理開始')
        user = User(user_id=form.user_id.data, email=form.email.data,
                    password=form.password.data, profile=Profile())
        db.session.add(user)
        db.session.commit()
        flash('登録しました。ログインしてください。', 'success')
        return redirect(url_for('auth_view.login'))

    return render_template('signup.html', form=form)
