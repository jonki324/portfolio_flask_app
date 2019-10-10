from application.models.base import Base, db


class Profile(Base):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    nickname = db.Column(db.String(80))
    comment = db.Column(db.String(200))
    icon = db.Column(db.Binary)

    user = db.relationship('User', back_populates='profile')

    def __init__(self, user_id=None, nickname=None, comment=None, icon=None):
        self.user_id = user_id
        self.nickname = nickname
        self.comment = comment
        self.icon = icon

    def __repr__(self):
        return '<Profile id: {}, user_id: {}, nickname: {}>'.format(self.id, self.user_id,
                                                                    self.nickname)
