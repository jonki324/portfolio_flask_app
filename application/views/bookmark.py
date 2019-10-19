from application.models.bookmark_post import BookmarkPost, db
from application.models.user import User, bookmark_users
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for, jsonify)
from flask_login import login_required, current_user

bookmark_view = Blueprint('bookmark_view', __name__)


@bookmark_view.route('/bookmark/post/add', methods=['POST'])
@login_required
def add_post():
    current_app.logger.info('記事ブックマーク登録処理開始')

    post_id = request.form['post_id']

    msg = '登録済みです'

    cnt = db.session.query(BookmarkPost).filter(BookmarkPost.user_id == current_user.id,
                                                BookmarkPost.bookmark_post_id == post_id).count()

    if cnt == 0:
        bookmark_post = BookmarkPost(user_id=current_user.id, bookmark_post_id=post_id)
        db.session.add(bookmark_post)
        db.session.commit()

        msg = '登録しました'

    bookmark_cnt = db.session.query(BookmarkPost).filter(BookmarkPost.bookmark_post_id == post_id).count()

    return jsonify({'bookmark_count': bookmark_cnt,
                    'msg': msg,
                    'del_flg': True})


@bookmark_view.route('/bookmark/post/rmv', methods=['POST'])
@login_required
def rmv_post():
    current_app.logger.info('記事ブックマーク削除処理開始')

    post_id = request.form['post_id']

    msg = '解除済みです'

    bookmark_post = db.session.query(BookmarkPost).filter(BookmarkPost.user_id == current_user.id,
                                                          BookmarkPost.bookmark_post_id == post_id).first()
    if bookmark_post:
        db.session.delete(bookmark_post)
        db.session.commit()

        msg = '解除しました'

    bookmark_cnt = db.session.query(BookmarkPost).filter(BookmarkPost.bookmark_post_id == post_id).count()

    return jsonify({'bookmark_count': bookmark_cnt,
                    'msg': msg,
                    'del_flg': False})


@bookmark_view.route('/bookmark/user/add', methods=['POST'])
@login_required
def add_user():
    current_app.logger.info('ユーザブックマーク登録処理開始')

    user_id = request.form['user_id']

    msg = '登録済みです'

    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')]).where(
        db.and_(bookmark_users.c.bookmark_user_id == user_id, bookmark_users.c.user_id == current_user.id))
    result = db.engine.execute(stmt)
    cnt = result.fetchone()['cnt']

    if cnt == 0:
        db.engine.execute(bookmark_users.insert().values(user_id=current_user.id, bookmark_user_id=user_id))

        msg = '登録しました'

    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')]).where(
        bookmark_users.c.bookmark_user_id == user_id)
    result = db.engine.execute(stmt)
    bookmark_cnt = result.fetchone()['cnt']

    return jsonify({'bookmark_count': bookmark_cnt,
                    'msg': msg,
                    'del_flg': True})


@bookmark_view.route('/bookmark/user/rmv', methods=['POST'])
@login_required
def rmv_user():
    current_app.logger.info('ユーザブックマーク削除処理開始')

    user_id = request.form['user_id']

    msg = '解除済みです'

    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')]).where(
        db.and_(bookmark_users.c.bookmark_user_id == user_id, bookmark_users.c.user_id == current_user.id))
    result = db.engine.execute(stmt)
    cnt = result.fetchone()['cnt']
    if cnt > 0:
        stmt = bookmark_users.delete().where(db.and_(bookmark_users.c.bookmark_user_id == user_id,
                                                     bookmark_users.c.user_id == current_user.id))
        db.engine.execute(stmt)

        msg = '解除しました'

    stmt = db.select([db.func.count(bookmark_users.c.bookmark_user_id).label('cnt')]).where(
        bookmark_users.c.bookmark_user_id == user_id)
    result = db.engine.execute(stmt)
    bookmark_cnt = result.fetchone()['cnt']

    return jsonify({'bookmark_count': bookmark_cnt,
                    'msg': msg,
                    'del_flg': False})
