from application.models.base import Base, db


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    image = db.Column(db.Binary, nullable=False)

    author = db.relationship('User', back_populates='posts')

    def __init__(self, author_id, title, body, image):
        self.author_id = author_id
        self.title = title
        self.body = body
        self.image = image

    def __repr__(self):
        return '<Post id: {}, author_id: {}, title: {}>'.format(self.id, self.author_id,
                                                                self.title)
