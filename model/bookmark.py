import bcrypt
import jwt
from flask import jsonify, request
import datetime
from .database import db, ma


class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    ani_id = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __init__(self, uid, ani_id, score):
        self.uid = uid
        self.ani_id = ani_id
        self.score = score

    @property
    def serialize(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'ani_id': self.ani_id,
            'score': self.score,
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]


class BookmarkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'uid', 'ani_id', 'score')

