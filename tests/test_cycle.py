from test_utils import TestCase
from account_model.category import Category
from account_model.account import *
from account_model.cycle import Cycle
from account_api.data_initializer import DataInitializer
import uuid
import datetime


CURRENT_TIME = datetime.datetime.now()
CURRENT_TIME_TRUNC = CURRENT_TIME.replace(hour=0, minute=0, second=0, microsecond=0)
START_DATE = datetime.datetime(2015, 10, 25)

__author__ = 'jtomaszk'

USER_ID = uuid.uuid4()
USER_ID_2 = uuid.uuid4()
CATEGORY_ID = uuid.uuid4()
ACCOUNT_ID = uuid.uuid4()
TYPE = 'INCOME'


class TestCycle(TestCase):

    item = None
    cat = Category
    CURRENCY_ID = None

    def setUp(self):
        TestCase.setUp(self)
        DataInitializer() \
            .init_categories(USER_ID)
        self.CURRENCY_ID = Currency('XXX', USER_ID).add().id
        self.item = Cycle(ACCOUNT_ID, 'test name', CURRENT_TIME, 'years', 10, 200, CATEGORY_ID, TYPE)

    def test_added_is_active(self):
        # when
        self.item.add().flush()
        # then
        self.assertTrue(self.item.active)

    def test_added_is_have_no_executions(self):
        # when
        self.item.add().flush()
        # then
        self.assertIsNone(self.item.date_last)
        self.assertEqual(0, self.item.count)

    def test_added_have_truncated_dates(self):
        # when
        self.item.add().flush()
        # then
        self.assertEquals(self.item.date_start, CURRENT_TIME_TRUNC)
        self.assertEquals(self.item.date_next, CURRENT_TIME_TRUNC)

    def test_calculate_proper_delta(self):
        # given
        start_date = datetime.datetime(2015, 10, 25, 11, 51, 22)
        self.item.add().flush()
        # when
        ret = self.item.calculate_delta() + start_date
        # then
        self.assertEqual(ret, datetime.datetime(2025, 10, 25, 11, 51, 22))

    def test_calculate_next_date_when_first_time(self):
        # given
        self.item.add().flush()
        self.item.date_start = START_DATE
        self.item.repeat_type = 'weeks'
        # when
        ret = self.item.calculate_next()
        # then
        self.assertEqual(ret, START_DATE)

    def test_calculate_next_date_when_second_time(self):
        # given
        self.item.add().flush()
        self.item.date_start = datetime.datetime(2010, 1, 1)
        self.item.repeat_type = 'weeks'
        self.item.repeat_every = 2
        self.item.date_last = datetime.datetime(2015, 12, 1)
        # when
        ret = self.item.calculate_next()
        # then
        self.assertEqual(ret, datetime.datetime(2010, 1, 15))

    def test_is_completed_when_last_date_equal_end(self):
        # given
        self.item.add().flush()
        end_date = datetime.datetime(2015, 12, 1)
        self.item.date_end = end_date
        self.item.date_last = end_date
        # when
        ret = self.item.is_completed()
        # then
        self.assertTrue(ret)

    def test_it_is_not_completed_before_start(self):
        # given
        self.item.add().flush()
        end_date = datetime.datetime(2015, 12, 1)
        self.item.date_end = end_date
        # when
        ret = self.item.is_completed()
        # then
        self.assertFalse(ret)

    def test_it_is_not_completed_before_end(self):
        # given
        self.item.add().flush()
        end_date = datetime.datetime(2015, 12, 1)
        self.item.date_end = end_date
        self.item.date_last = datetime.datetime(2015, 11, 1)
        # when
        ret = self.item.is_completed()
        # then
        self.assertFalse(ret)

    def test_it_is_not_completed_when_endless(self):
        # given
        self.item.add().flush()
        self.item.date_last = datetime.datetime(2015, 11, 1)
        # when
        ret = self.item.is_completed()
        # then
        self.assertFalse(ret)

    def test_is_completed_when_max_occurs(self):
        # given
        self.item.add().flush()
        self.item.date_last = datetime.datetime(2015, 11, 1)
        self.item.max_count = 10
        self.item.count = 10
        # when
        ret = self.item.is_completed()
        # then
        self.assertTrue(ret)

    def test_when_executed_last_date_updated(self):
        # given
        self.item.add().flush()
        next_date = self.item.calculate_next()
        # when
        self.item.save_execute(next_date)
        # then
        self.assertEquals(self.item.date_last, CURRENT_TIME_TRUNC)
        self.assertEquals(self.item.count, 1)

    def test_when_cycle_completed_is_going_inactive(self):
        # given
        self.item.max_count = 1
        self.item.add().flush()
        next_date = self.item.calculate_next()
        # when
        self.item.save_execute(next_date)
        # then
        self.assertFalse(self.item.active)

