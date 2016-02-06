from flask import Blueprint
import uuid
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

    def __init__(self, name, email, picture, oauth2_id):
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.picture = picture
        self.oauth2_id = oauth2_id

    @classmethod
    def get_by_oauth2_id(cls, oauth2_id):
        return cls.query.filter_by(oauth2_id=oauth2_id).first()

    @classmethod
    def add(cls, name, email, picture, oauth2_id):
        user = User(name, email, picture, oauth2_id)
        db.session.add(user)
        return user








