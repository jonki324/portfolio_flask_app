from application.forms.profile import ProfileForm
from application.models.user import User, db
from application.models.profile import Profile
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

profile_view = Blueprint('profile_view', __name__)


@profile_view.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    current_app.logger.info('プロフィール処理開始')
    form = ProfileForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('プロフィール更新処理開始')

        user = db.session.query(User).filter(User.id == current_user.id).first()
        user.profile.nickname = form.nickname.data
        user.profile.comment = form.comment.data
        user.profile.icon = form.icon.data.read()

        db.session.add(user)
        db.session.commit()

        flash('プロフィールを更新しました。', 'success')
        return redirect(url_for('index'))

    return render_template('profile.html', form=form)
