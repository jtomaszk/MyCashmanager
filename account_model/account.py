import uuid
import datetime
from sqlalchemy_utils import UUIDType

from database.numeric_type import SqliteNumeric
from account_model.transaction import Transaction
from account_model.currency import Currency
from database.serializer import *
from auth_model.user import User
from account_model.user_aware import UserAware

__author__ = 'jtomaszk'


class Account(db.Model, Serializer, UserAware):
    id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String(200))
    deleted = db.Column(db.Boolean)
    currency_id = db.Column(UUIDType(binary=False), db.ForeignKey(Currency.id))
    currency = db.relationship(Currency)
    user_id = db.Column(UUIDType(binary=False), db.ForeignKey(User.id))
    transactions = db.relationship(Transaction)
    balance = db.Column(SqliteNumeric)

    def __init__(self, user_id, currency_id, name):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.currency_id = currency_id
        self.name = name
        self.balance = 0

    def serialize_extra_column(self):
        return {
            "currency_name": self.currency.name
        }

    @classmethod
    def get_account(cls, account_id, user_id):
        return cls.query \
            .filter(Account.user_id.is_(user_id)) \
            .filter(Account.id.is_(account_id)) \
            .one()

    def add_income(self, amount, category_id, comment='', date=datetime.datetime.now()):
        transaction = Transaction(self.id, amount, 'INCOME', category_id)
        transaction.comment = comment
        transaction.date = date
        transaction.add()
        self.balance += amount
        return transaction

    def add_outcome(self, amount, category_id, comment='', date=datetime.datetime.now()):
        transaction = Transaction(self.id, amount, 'OUTCOME', category_id)
        transaction.comment = comment
        transaction.date = date
        transaction.add()
        self.balance -= amount
        return transaction

    def check_balance(self):
        balance = 0
        for i in self.transactions:
            if i.transaction_type == 'INCOME':
                balance += i.amount
            elif i.transaction_type == 'OUTCOME':
                balance -= i.amount
            else:
                balance += i.amount
        return balance
