from application.forms.blog import BlogForm
from application.models.user import User, db, bookmark_users
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user

blog_view = Blueprint('blog_view', __name__)


@blog_view.route('/blog/<user_id>')
def blog(user_id):
    current_app.logger.info('マイブログ処理開始')

    bookmark_search = request.args.get('bookmark', default=False)
    keyword = request.args.get('keyword', default='')

    form = BlogForm(keyword=keyword)

    user = db.session.query(User).filter(User.user_id == user_id).first()

    profile = user.profile

    bmk_users = user.bookmark_users

    if bookmark_search:
        posts = []
        bmk_posts = user.bookmark_posts
        for post in bmk_posts:
            posts.append(post.bookmark_posts)
    elif keyword != '':
        posts = db.session.query(BlogPost).filter(BlogPost.author_id == user.id,
                                                  db.or_(BlogPost.title.like('%{}%'.format(keyword)),
                                                         BlogPost.body.like('%{}%'.format(keyword)))).\
            order_by(BlogPost.created_at.desc()).all()
    else:
        posts = user.posts

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = posts[(page - 1) * 9: page * 9]
    pagination = Pagination(page=page, total=len(posts), per_page=9, css_framework='bootstrap4', alignment='center')

    bookmarks = []
    if current_user.is_authenticated:
        cur_user = db.session.query(User).filter(User.id == current_user.id).first()
        bookmarks = cur_user.bookmark_posts

    bookmark_info = {}
    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')]).where(
        bookmark_users.c.bookmark_user_id == user.id)
    result = db.engine.execute(stmt)
    bookmark_count = result.fetchone()['cnt']
    bookmark_info['bookmark_count'] = bookmark_count

    if current_user.is_authenticated and current_user.user_id != user_id:
        stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')]).where(
            db.and_(bookmark_users.c.bookmark_user_id == user.id, bookmark_users.c.user_id == current_user.id))
        result = db.engine.execute(stmt)
        is_bookmark = result.fetchone()['cnt']

        bookmark_info['is_bookmark'] = bool(is_bookmark)

    return render_template('blog.html', form=form, user=user, bmk_users=bmk_users, bookmarks=bookmarks, bookmark_info=bookmark_info, profile=profile, posts=res, pagination=pagination)
