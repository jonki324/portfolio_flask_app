from application.models.base import Base, db


class BookmarkUser(Base):
    __tablename__ = 'bookmarks_user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bookmark_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='bookmarks_user',
                           primayjoin='User.id == BookmarkUser.user_id')
    bookmark_user = db.relationship('User', uselist=False,
                                    primayjoin='User.id == BookmarkUser.bookmark_user_id')

    def __init__(self, user_id, bookmark_user_id):
        self.user_id = user_id
        self.bookmark_user_id = bookmark_user_id

    def __repr__(self):
        return '<BookmarkUser id: {}, user_id: {}, bookmark_id: {}>'.format(self.id,
                                                                            self.user_id,
                                                                            self.bookmark_user_id)
