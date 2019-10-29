from application.models.bookmark_post import BookmarkPost, db
from application.models.user import bookmark_users
from flask import Blueprint, current_app, request, jsonify
from flask_login import login_required, current_user

bookmark_view = Blueprint('bookmark_view', __name__)


@bookmark_view.route('/bookmark/post/add', methods=['POST'])
@login_required
def add_post():
    current_app.logger.info('記事ブックマーク登録処理開始')

    post_id = request.form['post_id']

    msg = '登録済みです'

    bookmark_post_count = fetch_current_users_bookmark_post_by_post_id(post_id).count()
    if bookmark_post_count == 0:
        current_app.logger.info('記事ブックマーク登録')
        bookmark_post = BookmarkPost(user_id=current_user.id, bookmark_post_id=post_id)
        db.session.add(bookmark_post)
        db.session.commit()

        msg = '登録しました'

    bookmark_count = fetch_bookmark_post_count_by_post_id(post_id)

    return jsonify({'bookmark_count': bookmark_count,
                    'msg': msg,
                    'del_flg': True})


@bookmark_view.route('/bookmark/post/rmv', methods=['POST'])
@login_required
def rmv_post():
    current_app.logger.info('記事ブックマーク削除処理開始')

    post_id = request.form['post_id']

    msg = '解除済みです'

    bookmark_post = fetch_current_users_bookmark_post_by_post_id(post_id).first()
    if bookmark_post:
        current_app.logger.info('記事ブックマーク削除')
        db.session.delete(bookmark_post)
        db.session.commit()

        msg = '解除しました'

    bookmark_count = fetch_bookmark_post_count_by_post_id(post_id)

    return jsonify({'bookmark_count': bookmark_count,
                    'msg': msg,
                    'del_flg': False})


@bookmark_view.route('/bookmark/user/add', methods=['POST'])
@login_required
def add_user():
    current_app.logger.info('ユーザーブックマーク登録処理開始')

    user_id = request.form['user_id']

    msg = '登録済みです'

    bookmark_user_count = fetch_current_users_bookmark_user_count_by_user_id(user_id)
    if bookmark_user_count == 0:
        current_app.logger.info('ユーザーブックマーク登録')
        add_bookmark_user_to_current_user(user_id)

        msg = '登録しました'

    bookmark_count = fetch_bookmark_user_count_by_user_id(user_id)

    return jsonify({'bookmark_count': bookmark_count,
                    'msg': msg,
                    'del_flg': True})


@bookmark_view.route('/bookmark/user/rmv', methods=['POST'])
@login_required
def rmv_user():
    current_app.logger.info('ユーザーブックマーク削除処理開始')

    user_id = request.form['user_id']

    msg = '解除済みです'

    bookmark_user_count = fetch_current_users_bookmark_user_count_by_user_id(user_id)
    if bookmark_user_count > 0:
        current_app.logger.info('ユーザーブックマーク削除')
        remove_bookmark_user_from_current_user(user_id)

        msg = '解除しました'

    bookmark_count = fetch_bookmark_user_count_by_user_id(user_id)

    return jsonify({'bookmark_count': bookmark_count,
                    'msg': msg,
                    'del_flg': False})


def fetch_current_users_bookmark_post_by_post_id(post_id):
    query = db.session.query(BookmarkPost)
    query = query.filter(BookmarkPost.user_id == current_user.id,
                         BookmarkPost.bookmark_post_id == post_id)
    return query


def fetch_bookmark_post_count_by_post_id(post_id):
    query = db.session.query(BookmarkPost)
    query = query.filter(BookmarkPost.bookmark_post_id == post_id)
    return query.count()


def fetch_current_users_bookmark_user_count_by_user_id(user_id):
    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')])
    stmt = stmt.where(db.and_(bookmark_users.c.bookmark_user_id == user_id,
                              bookmark_users.c.user_id == current_user.id))
    result = db.engine.execute(stmt)
    return result.fetchone()['cnt']


def fetch_bookmark_user_count_by_user_id(user_id):
    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')])
    stmt = stmt.where(bookmark_users.c.bookmark_user_id == user_id)
    result = db.engine.execute(stmt)
    return result.fetchone()['cnt']


def add_bookmark_user_to_current_user(insert_user_id):
    stmt = bookmark_users.insert()
    stmt = stmt.values(user_id=current_user.id,
                       bookmark_user_id=insert_user_id)
    db.engine.execute(stmt)


def remove_bookmark_user_from_current_user(remove_user_id):
    stmt = bookmark_users.delete()
    stmt = stmt.where(db.and_(bookmark_users.c.bookmark_user_id == remove_user_id,
                              bookmark_users.c.user_id == current_user.id))
    db.engine.execute(stmt)
