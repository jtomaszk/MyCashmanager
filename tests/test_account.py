from test_utils import TestCase
from account_model.category import Category
from account_model.account import *
from account_api.data_initializer import DataInitializer
import uuid

__author__ = 'jtomaszk'

USER_ID = uuid.uuid4()
USER_ID_2 = uuid.uuid4()
CATEGORY_ID = uuid.uuid4()


class TestAccount(TestCase):

    cat = Category
    CURRENCY_ID = None

    def setUp(self):
        TestCase.setUp(self)
        DataInitializer() \
            .init_categories(USER_ID)
        self.CURRENCY_ID = Currency('XXX', USER_ID).add().id

    def test_add_account(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa').add().flush()
        self.assertIsNotNone(account.id)
        self.assertEqual(account.currency.name, 'XXX')

    def test_check_balance_empty(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa').add()
        self.assertEqual(account.check_balance(), 0)

    def test_add_income(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa').add()
        account.add_income(Decimal('100.45'), CATEGORY_ID)
        account.add_income(Decimal('99.009'), CATEGORY_ID)
        account.add_income(Decimal('0.001'), CATEGORY_ID)
        self.assertEqual(account.check_balance(), Decimal('199.46'))

    def test_add_outcome(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa').add()
        account.add_income(Decimal('100'), CATEGORY_ID)
        account.add_outcome(Decimal('0.000001'), CATEGORY_ID)
        self.assertEqual(account.check_balance(), Decimal('99.999999'))

    def test_account_list(self):
        Account(USER_ID, self.CURRENCY_ID, 'nazwa').add()
        Account(USER_ID, self.CURRENCY_ID, 'nazwa2').add()
        Account(USER_ID_2, self.CURRENCY_ID, 'nazwa3').add()

        accounts = Account.all(USER_ID)

        self.assertEqual(accounts[0].name, 'nazwa')
        self.assertEqual(accounts[1].name, 'nazwa2')

    def test_get(self):
        Account(USER_ID_2, self.CURRENCY_ID, 'nazwa').add()
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa2').add()

        result = Account.get(account.id)

        self.assertEqual(result.name, 'nazwa2')

    def test_serialize(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa2').add().flush()
        result = account.serialize()
        self.assertDictContainsSubset({'currency_name': 'XXX'}, result)

    def test_balance_zero(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa2').add()
        self.assertEqual(account.balance, 0)

    def test_balance_sum(self):
        account = Account(USER_ID, self.CURRENCY_ID, 'nazwa2').add()
        account.add_income(Decimal('99.000009'), CATEGORY_ID)
        account.add_outcome(Decimal('0.000001'), CATEGORY_ID)
        self.assertEqual(account.balance, Decimal('99.000008'))
