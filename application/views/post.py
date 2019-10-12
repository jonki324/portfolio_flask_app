from application.forms.post import PostForm
from application.models.user import User, db
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_login import login_required, current_user

post_view = Blueprint('post_view', __name__)


@post_view.route('/post/add', methods=['GET', 'POST'])
@login_required
def add():
    current_app.logger.info('記事投稿処理開始')

    form = PostForm()

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('記事投稿処理開始')

        user = db.session.query(User).filter(User.id == current_user.id).first()

        post = BlogPost(title=form.title.data, body=form.body.data, image=form.image.data.read())

        user.posts.append(post)

        db.session.add(user)
        db.session.commit()

        flash('投稿しました。', 'success')
        return redirect(url_for('blog_view.blog', user_id=current_user.user_id))

    return render_template('post.html', form=form)


@post_view.route('/post/upd/<post_id>', methods=['GET', 'POST'])
@login_required
def upd(post_id):
    current_app.logger.info('記事更新処理開始')

    try:
        user, post = db.session.query(User, BlogPost).filter(db.and_(User.id == current_user.id,
                                                                     BlogPost.id == post_id)).first()
    except Exception:
        flash('記事がありません。', 'danger')
        return redirect(url_for('blog_view.blog', user_id=current_user.user_id))

    form = PostForm(obj=post, is_img_saved='y')

    if request.method == 'POST' and form.validate_on_submit():
        current_app.logger.info('記事更新処理開始')
        post.title = form.title.data
        post.body = form.body.data
        if form.image.data:
            post.image = form.image.data.read()

        db.session.add(post)
        db.session.commit()

        flash('更新しました。', 'success')
        return redirect(url_for('blog_view.blog', user_id=current_user.user_id))

    return render_template('post.html', form=form)
