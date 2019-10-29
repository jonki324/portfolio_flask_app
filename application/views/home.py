from application.forms.index import IndexForm
from application.models.user import User, db
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app,
                   render_template, request)
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user

home_view = Blueprint('home_view', __name__)

PER_PAGE = 12


@home_view.route('/')
def index():
    current_app.logger.info('ホーム画面処理開始')

    keyword = request.args.get('keyword', default='')
    current_app.logger.info('キーワード: {}'.format(keyword))

    form = IndexForm(request.args)

    posts = []
    if keyword != '':
        if form.validate():
            current_app.logger.info('キーワード検索処理開始: {}'.format(keyword))
            posts = fetch_post_by_keyword(keyword)
    else:
        current_app.logger.info('記事全件検索処理開始')
        posts = fetch_all_post()

    posts, pagination = get_pagination(posts)

    current_user_bookmarks = []
    if current_user.is_authenticated:
        current_app.logger.info('ログインユーザーのブックマーク記事取得処理開始')
        current_user_bookmarks = get_current_user_bookmarks()

    return render_template('index.html', form=form,
                           posts=posts, pagination=pagination,
                           current_user_bookmarks=current_user_bookmarks)


def fetch_post_by_keyword(keyword):
    query = db.session.query(BlogPost)
    query = query.filter(db.or_(BlogPost.title.like('%{}%'.format(keyword)),
                                BlogPost.body.like('%{}%'.format(keyword))))
    query = query.order_by(BlogPost.created_at.desc())
    return query.all()


def fetch_all_post():
    query = db.session.query(BlogPost)
    query = query.order_by(BlogPost.created_at.desc())
    return query.all()


def get_pagination(posts):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(posts), per_page=PER_PAGE,
                            css_framework='bootstrap4', alignment='center')
    res = posts[(page - 1) * PER_PAGE: page * PER_PAGE]
    return res, pagination


def get_current_user_bookmarks():
    cur_user = db.session.query(User).filter(User.id == current_user.id).first()
    return cur_user.bookmark_posts
