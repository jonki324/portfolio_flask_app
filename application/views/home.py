from application.forms.index import IndexForm
from application.models.user import User, db
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user

home_view = Blueprint('home_view', __name__)


@home_view.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.info('ブログ検索処理開始')

    keyword = request.args.get('keyword', default='')

    form = IndexForm(keyword=keyword)

    if keyword != '':
        posts = db.session.query(BlogPost).filter(db.or_(BlogPost.author_id.like('%{}%'.format(keyword)),
                                                         BlogPost.title.like('%{}%'.format(keyword)),
                                                         BlogPost.body.like('%{}%'.format(keyword)))).\
            order_by(BlogPost.created_at.desc()).all()
    else:
        posts = db.session.query(BlogPost).order_by(BlogPost.created_at.desc()).all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = posts[(page - 1) * 12: page * 12]
    pagination = Pagination(page=page, total=len(posts), per_page=12, css_framework='bootstrap4', alignment='center')

    bookmarks = []
    if current_user.is_authenticated:
        cur_user = db.session.query(User).filter(User.id == current_user.id).first()
        bookmarks = cur_user.bookmark_posts

    return render_template('index.html', form=form, bookmarks=bookmarks, posts=res, pagination=pagination)
