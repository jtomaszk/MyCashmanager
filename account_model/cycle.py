import uuid
import datetime
from sqlalchemy_utils import UUIDType
from dateutil.relativedelta import relativedelta

from database.numeric_type import SqliteNumeric
from database.serializer import Serializer
from database.serializer import db

__author__ = 'jtomaszk'


def trunc_date(date_value):
    return datetime.date(date_value.year, date_value.month, date_value.day)


class Cycle(db.Model, Serializer):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    account_id = db.Column(UUIDType(binary=False), db.ForeignKey('account.id'))
    account = db.relationship('Account')
    category_id = db.Column(UUIDType(binary=False), db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('cycles', lazy='dynamic'))
    transaction_type = db.Column(db.Enum('INCOME', 'OUTCOME'))
    name = db.Column(db.String(200), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date)
    date_last = db.Column(db.Date)
    date_next = db.Column(db.Date)
    count = db.Column(db.Integer, default=0)
    max_count = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)
    repeat_type = db.Column(db.Enum('days', 'weeks', 'months', 'years'))
    repeat_every = db.Column(db.Integer)
    amount = db.Column(SqliteNumeric)

    def __init__(self,
                 account_id,
                 name,
                 date_start,
                 repeat_type,
                 repeat_every,
                 amount,
                 category_id,
                 transaction_type,
                 max_count=None,
                 date_end=None):
        self.id = uuid.uuid4()
        self.account_id = account_id
        self.name = name
        date_start_truncated = trunc_date(date_start)
        self.date_start = date_start_truncated
        self.date_next = date_start_truncated
        self.repeat_type = repeat_type
        self.repeat_every = repeat_every
        self.amount = amount
        self.category_id = category_id
        self.transaction_type = transaction_type
        self.max_count = max_count
        if date_end is not None:
            date_end = trunc_date(date_end)
        self.date_end = date_end

    def serialize_extra_column(self):
        return {
            "category_name": self.category.name,
            "account_name": self.account.name,
            "account_currency_name": self.account.currency.name
        }

    def is_completed(self):
        if not self.active:
            return True
        if self.date_end is not None and self.date_last is not None and self.date_last >= self.date_end:
            return True
        elif self.max_count is not None and self.count >= self.max_count:
            return True
        else:
            return False

    def calculate_next(self):
        if self.is_completed():
            return None
        elif self.date_last is None:
            return self.date_start
        else:
            return self.calculate_delta() * (self.count + 1) + self.date_start

    def save_execute(self, date_executed):
        self.date_last = trunc_date(date_executed)
        self.count += 1

        if self.is_completed():
            self.active = False

    def calculate_delta(self):
        rd = relativedelta()

        if self.repeat_type == 'days':
            rd.days = self.repeat_every
        elif self.repeat_type == 'weeks':
            rd.days = self.repeat_every * 7
        elif self.repeat_type == 'months':
            rd.months = self.repeat_every
        elif self.repeat_type == 'years':
            rd.years = self.repeat_every

        return rd

    @classmethod
    def all(cls, user_id):
        return cls.query.join('account').filter_by(user_id=user_id).all()

