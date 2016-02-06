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
            Category('None', user_id).add()
            Category('Food - shop', user_id).add()
            Category('Food - restaurants', user_id).add()
            Category('Home - bills', user_id).add()
            Category('Home - other', user_id).add()
            Category('Income - regular', user_id).add()
            Category('Income - other', user_id).add()
            Category('Entertainment - cinema, theatre', user_id).add()
            Category('Entertainment - restaurants, pubs', user_id).add()
            Category('Entertainment - other', user_id).add()
            Category('Car - fuel', user_id).add()
            Category('Car - services', user_id).add()
            Category('Car - parking', user_id).add()
            Category('Car - insurance', user_id).add()
            Category('Car - other', user_id).add()
            Category('Education', user_id).add()
            Category('Sport ', user_id).add()
            Category('Health ', user_id).add()
            Category('Beauty ', user_id).add()
            Category('Education ', user_id).add()
            Category('Personal ', user_id).add()
            Category('Other ', user_id).add()
            Category('Taxes ', user_id).add()
            Category('Insurance ', user_id).add()
            Category('Vacation - accommodation', user_id).add()
            Category('Vacation - transport', user_id).add()
            Category('Vacation - other', user_id).add()
        return self

    def init_currencies(self, user_id):
        if self.is_empty(Currency, user_id):
            Currency('PLN', user_id).add()
            Currency('EUR', user_id).add()
            Currency('USD', user_id).add()
        return self
