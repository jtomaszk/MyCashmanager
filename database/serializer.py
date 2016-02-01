from decimal import Decimal
import sqlalchemy.types as types

from database.config import db

PRECISION = 1000000

__author__ = 'jtomaszk'


class SqliteNumeric(types.TypeDecorator):

    def python_type(self):
        return Decimal

    def process_literal_param(self, value, dialect):
        if value is None:
            return None
        return int(value * Decimal(PRECISION))

    impl = types.Integer

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.Integer)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return int(value * Decimal(PRECISION))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return Decimal(value) / Decimal(PRECISION)


class Serializer(object):

    def serialize(self):
        columns = self.__table__.columns
        ret = dict((c.name, getattr(self, c.name)) for c in columns)
        extra = self.serialize_extra_column()
        ret = dict(ret, **extra)

        for key in ret.keys():
            if isinstance(ret[key], Decimal):
                ret[key] = float(ret[key])

        return ret

    def serialize_extra_column(self):
        return dict()

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.merge(self)
        db.session.commit()
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
