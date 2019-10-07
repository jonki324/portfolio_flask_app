from application.models.base import Base, db
from flask_login import UserMixin
from sqlalchemy.orm import synonym
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(80), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password.strip())
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User id: {}, name: {}, email: {}>'.format(self.id, self.name, self.email)

    def check_password(self, password):
        return check_password_hash(self.password, password.strip())

    @classmethod
    def auth(cls, query, email, password):
        user = query(cls).filter(cls.email == email).first()
        return user, user and user.check_password(password)
