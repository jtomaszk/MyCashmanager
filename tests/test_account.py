from decimal import *

from test_utils import TestCase
from account_model.category import Category
from account_model.account import *
from account_api.data_initializer import DataInitializer

__author__ = 'jtomaszk'

USER_ID = 12343
CURRENCY_ID = 1
CATEGORY_ID = 1


class TestAccount(TestCase):

    cat = Category

    def setUp(self):
        TestCase.setUp(self)
        DataInitializer() \
            .init_categories(USER_ID) \
            .init_currencies(USER_ID)

    def test_add_account(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa').add()
        self.assertIsNotNone(account.id)
        self.assertEqual(account.currency.name, 'PLN')

    def test_check_balance_empty(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa').add()
        self.assertEqual(account.check_balance(), 0)

    def test_add_income(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa').add()
        account.add_income(Decimal('100.45'), CATEGORY_ID)
        account.add_income(Decimal('99.009'), CATEGORY_ID)
        account.add_income(Decimal('0.001'), CATEGORY_ID)
        self.assertEqual(account.check_balance(), Decimal('199.46'))

    def test_add_outcome(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa').add()
        account.add_income(Decimal('100'), CATEGORY_ID)
        account.add_outcome(Decimal('0.000001'), CATEGORY_ID)
        self.assertEqual(account.check_balance(), Decimal('99.999999'))

    def test_account_list(self):
        Account(USER_ID, CURRENCY_ID, 'nazwa').add()
        Account(USER_ID, CURRENCY_ID, 'nazwa2').add()
        Account(2, CURRENCY_ID, 'nazwa3').add()

        accounts = Account.all(USER_ID)

        self.assertEqual(accounts[0].name, 'nazwa')
        self.assertEqual(accounts[1].name, 'nazwa2')

    def test_get(self):
        Account(22, CURRENCY_ID, 'nazwa').add()
        account = Account(USER_ID, CURRENCY_ID, 'nazwa2').add()

        result = Account.get_account(account.id, USER_ID)

        self.assertEqual(result.name, 'nazwa2')

    def test_serialize(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa2').add()
        result = account.serialize()
        self.assertDictContainsSubset({'currency_name': 'PLN'}, result)

    def test_balance_zero(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa2').add()
        self.assertEqual(account.balance, 0)

    def test_balance_sum(self):
        account = Account(USER_ID, CURRENCY_ID, 'nazwa2').add()
        account.add_income(Decimal('99.000009'), CATEGORY_ID)
        account.add_outcome(Decimal('0.000001'), CATEGORY_ID)
        self.assertEqual(account.balance, Decimal('99.000008'))
