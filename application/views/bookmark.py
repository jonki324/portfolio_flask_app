from application.models.bookmark_post import BookmarkPost, db
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for, jsonify)
from flask_login import login_required, current_user

bookmark_view = Blueprint('bookmark_view', __name__)


@bookmark_view.route('/bookmark/post/add', methods=['POST'])
@login_required
def add_post():
    current_app.logger.info('ブックマーク登録処理開始')

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
    current_app.logger.info('ブックマーク削除処理開始')

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
