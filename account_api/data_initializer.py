from account_model.category import *
from account_model.currency import *

__author__ = 'jtomaszk'


class DataInitializer:

    @staticmethod
    def is_empty(ob, user_id=0):
        if user_id == 0:
            return len(ob.all()) == 0
        else:
            return len(ob.all(user_id)) == 0

    def init_categories(self, user_id):
        if self.is_empty(Category, user_id):
            Category('Home', user_id).add()
            Category('Car', user_id).add()
        return self

    def init_currencies(self, user_id):
        if self.is_empty(Currency, user_id):
            Currency('PLN', user_id).add()
            Currency('EUR', user_id).add()
        return self
