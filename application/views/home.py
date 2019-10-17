from application.forms.index import IndexForm
from application.models.user import User, db
from application.models.blog_post import BlogPost
from flask import (Blueprint, current_app, flash,
                   redirect, render_template, request, url_for)
from flask_paginate import Pagination, get_page_parameter

home_view = Blueprint('home_view', __name__)


@home_view.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.info('ブログ検索処理開始')

    form = IndexForm()

    if request.method == 'POST' and form.validate_on_submit():
        keyword = form.keyword.data
        posts = db.session.query(BlogPost).filter(db.or_(BlogPost.author_id.like('%{}%'.format(keyword)),
                                                         BlogPost.title.like('%{}%'.format(keyword)),
                                                         BlogPost.body.like('%{}%'.format(keyword)))).\
            order_by(BlogPost.created_at.desc()).all()
    else:
        posts = db.session.query(BlogPost).order_by(BlogPost.created_at.desc()).all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    res = posts[(page - 1) * 10: page * 10]
    pagination = Pagination(page=page, total=len(posts), per_page=10, css_framework='bootstrap4', alignment='center')

    return render_template('index.html', form=form, posts=res, pagination=pagination)
