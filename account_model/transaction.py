import datetime
import uuid
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func

from database.numeric_type import SqliteNumeric
from database.serializer import Serializer
from database.serializer import db
from account_model.currency import Currency
from account_model.category import Category
from account_model.cycle import Cycle

__author__ = 'jtomaszk'


class Transaction(db.Model, Serializer):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    transaction_type = db.Column(db.Enum('INCOME', 'OUTCOME', 'TRANSFER'))
    transfer_id = db.Column(UUIDType(binary=False), db.ForeignKey('transaction.id'), index=True)
    cycle_id = db.Column(UUIDType(binary=False), db.ForeignKey(Cycle.id), index=True)
    category_id = db.Column(UUIDType(binary=False), db.ForeignKey(Category.id), index=True)
    category = db.relationship(Category, backref=db.backref('transactions', lazy='dynamic'))
    account_id = db.Column(UUIDType(binary=False), db.ForeignKey('account.id'), index=True)
    amount = db.Column(SqliteNumeric)
    amount_orig = db.Column(SqliteNumeric)
    orig_currency_id = db.Column(UUIDType(binary=False), db.ForeignKey(Currency.id))
    orig_currency = db.relationship(Currency)
    date = db.Column(db.DateTime)
    running_total = db.Column(SqliteNumeric)
    comment = db.Column(db.String)

    def __init__(self,
                 account_id,
                 amount,
                 transaction_type,
                 category_id,
                 amount_orig=None,
                 orig_currency_id=None,
                 date=datetime.datetime.now(),
                 comment=''):
        self.id = uuid.uuid4()
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.amount_orig = amount_orig
        self.orig_currency_id = orig_currency_id
        self.category_id = category_id
        self.date = date
        self.increment_current_total(account_id, amount, date)
        self.comment = comment

    def serialize_extra_column(self):
        return {
            "category_name": self.category.name
        }

    def increment_current_total(self, account_id, amount, date):
        current_total = self.get_current_total(account_id, date)
        if current_total is None:
            current_total = amount
        else:
            current_total = current_total + amount
        self.running_total = current_total

    def connect(self, other):
        self.transfer_id = other.id

    @staticmethod
    def get_current_total(account_id, date):
        current_total_result = Transaction.query_running_total(account_id, date)
        assert len(current_total_result) <= 1

        if len(current_total_result) == 1:
            current_total = current_total_result[0].running_total
            return current_total
        else:
            return None

    @staticmethod
    def query_running_total(account_id, date):
        current_total_result = db.session.query(func.sum(Transaction.amount).label('running_total')) \
            .filter(Transaction.account_id == account_id) \
            .filter(Transaction.date <= date) \
            .group_by(Transaction.account_id) \
            .all()
        return current_total_result
