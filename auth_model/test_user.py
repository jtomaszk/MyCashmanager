from test_utils import TestCase

from user import User

OAUTH2_ID = '213453'

__author__ = 'jtomaszk'

class TestUser(TestCase):

    def test_get_by_oauth2_id(self):
        user = User.get_by_oauth2_id(OAUTH2_ID)
        assert user is None

    def test_save_user(self):
        user = User.add('Jan', 'email', 'picture', OAUTH2_ID)
        assert user is not None

    def test_save_user_and_find(self):
        User.add('Jan', 'email', 'picture', OAUTH2_ID)
        user = User.get_by_oauth2_id(OAUTH2_ID)
        assert user is not None


