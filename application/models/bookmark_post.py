from application.models.base import Base, db


class BookmarkPost(Base):
    __tablename__ = 'bookmark_posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookmark_post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))

    user = db.relationship('User', back_populates='bookmark_posts')
    bookmark_posts = db.relationship('BlogPost', back_populates='users')

    def __init__(self, user_id, bookmark_post_id):
        self.user_id = user_id
        self.bookmark_post_id = bookmark_post_id

    def __repr__(self):
        return '<BookmarkPost id: {}, user_id: {}, bookmark_id: {}>'.format(self.id,
                                                                            self.user_id,
                                                                            self.bookmark_post_id)
