import uuid
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

    def add_income(self, amount, category_id, comment='', date=datetime.datetime.now()):
        self.increase_balance(amount)
        return self.create_and_add_transaction(amount, category_id, comment, date, 'INCOME')

    def increase_balance(self, amount):
        self.balance += amount

    def add_outcome(self, amount, category_id, comment='', date=datetime.datetime.now()):
        self.decrease_balance(amount)
        return self.create_and_add_transaction(amount, category_id, comment, date, 'OUTCOME')

    def create_and_add_transaction(self, amount, category_id, comment, date, transaction_type):
        return Transaction(self.id,
                           amount,
                           transaction_type,
                           category_id,
                           None,
                           None,
                           date,
                           comment) \
            .add()

    def decrease_balance(self, amount):
        self.balance -= amount

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
