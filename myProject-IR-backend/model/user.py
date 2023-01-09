from .database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    favorite = db.Column(db.Integer, nullable=True)
    bookmark = db.Column(db.Integer, nullable=True)

    def __init__(self, username, password, email, bookmark,favorite):
        self.username = username
        self.email = email
        self.password = password
        self.bookmark = bookmark
        self.favorite = favorite

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'bookmark': self.bookmark,
            'favorite': self.favorite
        }