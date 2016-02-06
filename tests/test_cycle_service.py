from account_api.cycle_service import *
from test_utils import TestCase
from account_model.account import *
from account_model.cycle import Cycle
from account_api.data_initializer import DataInitializer

CURRENT_TIME = datetime.datetime.now()
CURRENT_TIME_TRUNC = CURRENT_TIME.replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = datetime.datetime(2015, 10, 25)

__author__ = 'jtomaszk'

USER_ID = uuid.uuid4()
USER_ID_2 = uuid.uuid4()
CATEGORY_ID = uuid.uuid4()
ACCOUNT_ID = uuid.uuid4()
TYPE = 'INCOME'


class TestCycleService(TestCase):

    currency = None
    account = None
    cycle = None

    def setUp(self):
        TestCase.setUp(self)
        DataInitializer() \
            .init_categories(USER_ID)
        self.currency = Currency('XXX', USER_ID).add()
        self.account = Account(USER_ID, self.currency.id, 'test').add()
        self.cycle = Cycle(self.account.id, 'test cycle', CURRENT_TIME, 'days', 10, 200, CATEGORY_ID, TYPE)

    def test_execute_active_cycle(self):
        # given
        self.cycle.add().flush()
        # when
        ret = save_cycle_execution(self.cycle.id, 110, CURRENT_TIME,  self.account.id)
        # then
        self.assertEqual(self.account.balance, 110)
        self.assertEqual(ret.amount, 110)
        self.assertEqual(ret.category_id, CATEGORY_ID)
        self.assertEqual(ret.transaction_type, TYPE)
