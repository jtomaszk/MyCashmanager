import sqlalchemy.types as types
from decimal import Decimal

__author__ = 'jtomaszk'

PRECISION = 1000000

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