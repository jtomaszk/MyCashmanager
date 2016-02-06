import uuid
from sqlalchemy_utils import UUIDType

from database.serializer import *
from auth_model.user import User
from account_model.user_aware import UserAware

__author__ = 'jtomaszk'


class Category(db.Model, Serializer, UserAware):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String(200))
    user_id = db.Column(UUIDType(binary=False), db.ForeignKey(User.id))

    def __init__(self, name, user_id):
        self.id = uuid.uuid4()
        self.name = name
        self.user_id = user_id
