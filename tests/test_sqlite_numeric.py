from test_utils import TestCase
from database.numeric_type import SqliteNumeric
from database.config import db
from sqlalchemy.types import Integer

__author__ = 'jtomaszk'


class TestSqliteNumeric(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.column = db.Column(SqliteNumeric)

    def test_sql_type_is_integer(self):
        self.assertIsInstance(self.column.type.impl, Integer)

