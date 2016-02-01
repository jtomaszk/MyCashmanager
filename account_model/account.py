from account_model.transaction import Transaction
from account_model.currency import Currency
from database.serializer import *
from auth_model.user import User
from account_model.user_aware import UserAware

__author__ = 'jtomaszk'


class Account(db.Model, Serializer, UserAware):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    deleted = db.Column(db.Boolean)
    currency_id = db.Column(db.Integer, db.ForeignKey(Currency.id))
    currency = db.relationship(Currency)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    transactions = db.relationship(Transaction)
    balance = db.Column(SqliteNumeric)

    def __init__(self, user_id, currency_id, name):
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

    def add_income(self, amount, category_id, comment=''):
        transaction = Transaction(self.id, amount, amount, self.currency_id, category_id)
        transaction.type = 'INCOME'
        transaction.comment = comment
        db.session.add(transaction)
        self.balance += amount
        db.session.commit()

    def add_outcome(self, amount, category_id, comment=''):
        transaction = Transaction(self.id, amount, amount, self.currency_id, category_id)
        transaction.type = 'OUTCOME'
        transaction.comment = comment
        db.session.add(transaction)
        self.balance -= amount
        db.session.commit()

    def check_balance(self):
        balance = 0
        for i in self.transactions:
            if i.type == 'INCOME':
                balance += i.amount
            elif i.type == 'OUTCOME':
                balance -= i.amount
            else:
                balance += i.amount
        return balance
