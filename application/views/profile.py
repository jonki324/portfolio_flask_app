from application.forms.profile import ProfileForm
from application.models.user import User, db
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_login import login_required

profile_view = Blueprint('profile_view', __name__)


@profile_view.route('/profile', methods=['GET', 'POST'])
# @login_required
def profile():
    current_app.logger.info('プロフィール処理開始')
    form = ProfileForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('プロフィール更新処理開始')
        flash('プロフィールを更新しました。', 'success')
        return redirect(url_for('index'))

    return render_template('profile.html', form=form)
