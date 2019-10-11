from application.models.base import Base, db
from flask_login import UserMixin
from sqlalchemy.orm import synonym
from werkzeug.security import check_password_hash, generate_password_hash


bookmark_users = db.Table('bookmark_users', Base.metadata,
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                          db.Column('bookmark_user_id', db.Integer, db.ForeignKey('users.id'))
                          )


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(80), nullable=False)

    posts = db.relationship('BlogPost', back_populates='author')
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    bookmark_posts = db.relationship('BookmarkPost', back_populates='user')
    bookmark_users = db.relationship('User',
                                     secondary=bookmark_users,
                                     primaryjoin=id == bookmark_users.c.user_id,
                                     secondaryjoin=id == bookmark_users.c.bookmark_user_id)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password.strip())
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def __init__(self, user_id, email, password, profile):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.profile = profile

    def __repr__(self):
        return '<User id: {}, user_id: {}, email: {}>'.format(self.id, self.user_id, self.email)

    def check_password(self, password):
        return check_password_hash(self.password, password.strip())

    @classmethod
    def auth(cls, query, email, password):
        user = query(cls).filter(cls.email == email).first()
        return user, user and user.check_password(password)
