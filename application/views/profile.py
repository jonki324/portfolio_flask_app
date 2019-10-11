import base64
from application.forms.profile import ProfileForm
from application.models.user import User, db
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_login import login_required, current_user

profile_view = Blueprint('profile_view', __name__)


@profile_view.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    current_app.logger.info('プロフィール処理開始')
    user = db.session.query(User).filter(User.id == current_user.id).first()

    icon_bin = user.profile.icon
    icon = None
    if icon_bin:
        icon = base64.b64encode(icon_bin)
        icon = icon.decode("ascii")

    form = ProfileForm(obj=user.profile)

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('プロフィール更新処理開始')

        user.profile.nickname = form.nickname.data
        user.profile.comment = form.comment.data

        form_icon = form.icon.data.read()

        if form_icon != b'':
            user.profile.icon = form_icon
        else:
            if form.icon_del.data:
                user.profile.icon = None

        db.session.add(user)
        db.session.commit()

        flash('プロフィールを更新しました。', 'success')
        return redirect(url_for('blog_view.blog', user_id=current_user.user_id))

    return render_template('profile.html', form=form, icon=icon)
