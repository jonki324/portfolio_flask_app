from application.models.user import User, db
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)

blog_view = Blueprint('blog_view', __name__)


@blog_view.route('/blog/<user_id>')
def blog(user_id):
    current_app.logger.info('マイブログ処理開始')
    user = db.session.query(User).filter(User.user_id == user_id).first()

    profile = user.profile

    posts = user.posts

    return render_template('blog.html', profile=profile, posts=posts)
