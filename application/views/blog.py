import base64
# from application.forms.profile import ProfileForm
from application.models.user import User, db
# from application.models.profile import Profile
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_login import login_required, current_user

blog_view = Blueprint('blog_view', __name__)


@blog_view.route('/blog/<user_id>')
def blog(user_id):
    current_app.logger.info('マイブログ処理開始')
    user = db.session.query(User).filter(User.user_id == user_id).first()

    icon_bin = user.profile.icon
    icon = None
    if icon_bin:
        icon = base64.b64encode(icon_bin)
        icon = icon.decode("ascii")

    profile = {
        'user_id': user.user_id,
        'nickname': user.profile.nickname,
        'comment': user.profile.comment,
        'icon': icon
    }

    return render_template('blog.html', profile=profile)
