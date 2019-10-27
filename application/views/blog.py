from application.forms.blog import BlogForm
from application.models.user import User, db, bookmark_users
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app,
                   render_template, request)
from flask_paginate import Pagination, get_page_parameter
from flask_login import current_user

blog_view = Blueprint('blog_view', __name__)

PER_PAGE = 9


@blog_view.route('/blog/<user_id>')
def blog(user_id):
    current_app.logger.info('マイブログ処理開始')

    bookmark_search = request.args.get('bookmark', default=False)
    keyword = request.args.get('keyword', default='')

    form = BlogForm(request.args)

    user = fetch_blog_user_by_blog_user_id(user_id)

    profile = user.profile

    bookmark_users_by_blog_user = user.bookmark_users

    if bookmark_search:
        current_app.logger.info('ブログユーザーのブックマーク記事取得')
        posts = []
        bmk_posts = user.bookmark_posts
        for post in bmk_posts:
            posts.append(post.bookmark_posts)
    elif keyword != '':
        posts = []
        if form.validate():
            current_app.logger.info('キーワード検索処理開始: {}'.format(keyword))
            posts = fetch_blog_users_post_by_keyword(user.id, keyword)
    else:
        current_app.logger.info('ブログユーザーの記事全件取得')
        posts = user.posts

    posts, pagination = get_pagination(posts)

    current_user_bookmarks = []
    if current_user.is_authenticated:
        current_app.logger.info('ログインユーザーのブックマーク記事取得処理開始')
        current_user_bookmarks = fetch_bookmark_posts_from_current_user()

    profile_bookmark_info = {'bookmark_count': fetch_bookmark_user_count_target_blog_user(user.id),
                             'is_bookmarked': False}

    if current_user.is_authenticated and current_user.user_id != user_id:
        current_app.logger.info('ログインユーザーがブログユーザーをブックマークしているか')
        profile_bookmark_info['is_bookmarked'] = is_bookmarked_to_blog_user_from_cur_user(user.id)

    return render_template('blog.html', form=form, user=user, profile=profile,
                           bookmark_users_by_blog_user=bookmark_users_by_blog_user,
                           posts=posts, pagination=pagination,
                           current_user_bookmarks=current_user_bookmarks,
                           profile_bookmark_info=profile_bookmark_info)


def fetch_blog_user_by_blog_user_id(blog_user_id):
    query = db.session.query(User)
    query = query.filter(User.user_id == blog_user_id)
    return query.first()


def fetch_blog_users_post_by_keyword(blog_user_id, keyword):
    query = db.session.query(BlogPost)
    query = query.filter(BlogPost.author_id == blog_user_id,
                         db.or_(BlogPost.title.like('%{}%'.format(keyword)),
                                BlogPost.body.like('%{}%'.format(keyword))))
    query = query.order_by(BlogPost.created_at.desc())
    return query.all()


def get_pagination(posts):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(posts), per_page=PER_PAGE,
                            css_framework='bootstrap4', alignment='center')
    res = posts[(page - 1) * PER_PAGE: page * PER_PAGE]
    return res, pagination


def fetch_bookmark_posts_from_current_user():
    cur_user = db.session.query(User).filter(User.id == current_user.id).first()
    return cur_user.bookmark_posts


def fetch_bookmark_user_count_target_blog_user(blog_user_id):
    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')])
    stmt = stmt.where(bookmark_users.c.bookmark_user_id == blog_user_id)
    result = db.engine.execute(stmt)
    return result.fetchone()['cnt']


def is_bookmarked_to_blog_user_from_cur_user(blog_user_id):
    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')])
    stmt = stmt.where(db.and_(bookmark_users.c.bookmark_user_id == blog_user_id,
                              bookmark_users.c.user_id == current_user.id))
    result = db.engine.execute(stmt)
    return bool(result.fetchone()['cnt'])
