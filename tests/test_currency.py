from test_utils import TestCase
from account_model.currency import *

__author__ = 'jtomaszk'

USER_ID = 12343


class TestCurrency(TestCase):

    def setUp(self):
        TestCase.setUp(self)

    def test_add(self):
        Currency('PLN', USER_ID).add()

    def test_get_accounts(self):
        Currency('PLN', USER_ID).add()
        Currency('EUR', USER_ID).add()

        cur_list = Currency.all(USER_ID)

        self.assertEqual(len(cur_list), 2)
        self.assertEqual(cur_list[0].name, 'PLN')

    def test_get_accounts_other_user(self):
        Currency('PLN', USER_ID).add()

        cur_list = Currency.all(22)

        self.assertEqual(len(cur_list), 0)

