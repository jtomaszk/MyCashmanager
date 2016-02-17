import uuid

from flask import Blueprint
from sqlalchemy_utils import UUIDType

from database.serializer import *

__author__ = 'jtomaszk'

login_api = Blueprint('login_api', __name__)


class User(db.Model, Serializer):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    picture = db.Column(db.String(200))
    oauth2_id = db.Column(db.String(200))
    is_active = db.Column(db.Boolean)

    def __init__(self, name, email, picture, oauth2_id):
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.picture = picture
        self.oauth2_id = oauth2_id
        self.is_active = True

    @classmethod
    def get_by_oauth2_id(cls, oauth2_id):
        return cls.query.filter_by(oauth2_id=oauth2_id).first()

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)





