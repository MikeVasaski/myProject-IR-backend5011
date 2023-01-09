import bcrypt
from sqlalchemy import event
from .user import User
from .database import db


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(
        User(username='koonlookhin', password=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt(10)),
             email='lookhinganthe@hotmail.com',
             bookmark=None, favorite=None))
    db.session.commit()