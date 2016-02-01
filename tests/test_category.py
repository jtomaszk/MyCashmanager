from test_utils import TestCase
from account_model.category import *

USER_ID = 1

__author__ = 'jtomaszk'


class TestCategory(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test_add(self):
        val = Category('valVAA', USER_ID).add()

        self.assertEqual(val.id, 1)
        self.assertEqual(val.user_id, USER_ID)
        self.assertEqual(val.name, 'valVAA')

    def test_all(self):
        Category('valVAA', USER_ID).add()
        Category('valVAA34', USER_ID).add()

        ret = Category.all(USER_ID)

        self.assertEqual(len(ret), 2)

    def test_all_different_user(self):
        Category('valVAA', USER_ID).add()
        Category('valVAA34', USER_ID).add()

        ret = Category.all(2)

        self.assertEqual(len(ret), 0)
