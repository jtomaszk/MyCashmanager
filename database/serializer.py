from decimal import Decimal
import datetime
from time import mktime

from database.config import db

__author__ = 'jtomaszk'


class Serializer(object):

    def serialize(self):
        columns = self.__table__.columns
        ret = dict((c.name, getattr(self, c.name)) for c in columns)
        extra = self.serialize_extra_column()
        ret = dict(ret, **extra)

        for key in ret.keys():
            if isinstance(ret[key], Decimal):
                ret[key] = float(ret[key])
            elif isinstance(ret[key], datetime.date):
                ret[key] = mktime(ret[key].timetuple()) * 1e3
        return ret

    def serialize_extra_column(self):
        return dict()

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

    def commit(self):
        db.session.commit()
        return self

    def flush(self):
        db.session.flush()
        return self

    def add(self):
        db.session.add(self)
        return self

    def update(self):
        db.session.merge(self)
        return self

    @classmethod
    def get(cls, id):
        return cls.query \
            .filter(cls.id.is_(id)) \
            .one()


class Column(object):
    name = ''

    def __init__(self, name):
        self.name = name
