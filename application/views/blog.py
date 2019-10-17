from application.forms.blog import BlogForm
from application.models.user import User, db
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_paginate import Pagination, get_page_parameter

blog_view = Blueprint('blog_view', __name__)


@blog_view.route('/blog/<user_id>')
def blog(user_id):
    current_app.logger.info('マイブログ処理開始')

    keyword = request.args.get('keyword', default='')

    form = BlogForm(keyword=keyword)

    user = db.session.query(User).filter(User.user_id == user_id).first()

    profile = user.profile

    if keyword != '' and form.validate_on_submit():
        posts = db.session.query(BlogPost).filter(BlogPost.author_id == user.id,
                                                  db.or_(BlogPost.title.like('%{}%'.format(keyword)),
                                                         BlogPost.body.like('%{}%'.format(keyword)))).\
            order_by(BlogPost.created_at.desc()).all()
    else:
        posts = user.posts

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = posts[(page - 1) * 9: page * 9]
    pagination = Pagination(page=page, total=len(posts), per_page=9, css_framework='bootstrap4', alignment='center')

    return render_template('blog.html', form=form, profile=profile, posts=res, pagination=pagination)
