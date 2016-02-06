import datetime
from decimal import *
import uuid

from test_utils import TestCase
from account_model.transaction import Transaction


DATETIME = datetime.datetime.now()

CATEGORY_ID = uuid.uuid4()

TYPE = 'INCOME'

AMOUNT = Decimal('10.2')
AMOUNT_2 = Decimal('99.99')

ACCOUNT_ID = uuid.uuid4()

__author__ = 'jtomaszk'


class TestTransaction(TestCase):

    def set_up(self):
        TestCase.setUp(self)

    def test_construct(self):
        # account_id, amount, type, category_id, amount_orig, orig_currency_id, date
        ret = Transaction(ACCOUNT_ID, AMOUNT, TYPE, CATEGORY_ID, None, None, DATETIME)
        self.assertIsNotNone(ret.id)
        self.assertEqual(ret.account_id, ACCOUNT_ID)
        self.assertEqual(ret.amount, AMOUNT)
        self.assertEqual(ret.amount_orig, None)
        self.assertEqual(ret.orig_currency_id, None)
        self.assertEqual(ret.category_id, CATEGORY_ID)
        self.assertEqual(ret.date, DATETIME)
        self.assertEqual(ret.running_total, AMOUNT)

    def test_default_date(self):
        ret = Transaction(ACCOUNT_ID, AMOUNT, TYPE, CATEGORY_ID)
        self.assertIsNotNone(ret.date)

    def test_correct_running_sum(self):
        Transaction(ACCOUNT_ID, AMOUNT_2, TYPE, CATEGORY_ID).add()
        ret = Transaction(ACCOUNT_ID, AMOUNT, TYPE, CATEGORY_ID).add()
        self.assertEqual(AMOUNT + AMOUNT_2, ret.running_total)

    def test_correct_running_sum_substract(self):
        Transaction(ACCOUNT_ID, AMOUNT_2, TYPE, CATEGORY_ID).add()
        ret = Transaction(ACCOUNT_ID, -AMOUNT_2, TYPE, CATEGORY_ID).add()
        self.assertEqual(0, ret.running_total)
