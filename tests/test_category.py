from test_utils import TestCase
from account_model.category import *
import uuid

USER_ID = uuid.uuid4()
USER_ID_2 = uuid.uuid4()

__author__ = 'jtomaszk'


class TestCategory(TestCase):

    def test_add(self):
        val = Category('valVAA', USER_ID).add()

        self.assertIsNotNone(val.id)
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

        ret = Category.all(USER_ID_2)

        self.assertEqual(len(ret), 0)
