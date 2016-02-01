from database.config import db
from database.serializer import Serializer
from auth_model import user
from account_model.user_aware import UserAware


__author__ = 'jtomaszk'


class Currency(db.Model, Serializer, UserAware):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
