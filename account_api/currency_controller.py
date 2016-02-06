from flask import *

from account_model.currency import Currency
from account_api.data_initializer import DataInitializer

__author__ = 'jtomaszk'

currency_api = Blueprint('currency_api', __name__)

di = DataInitializer()


@currency_api.route('/currencies', methods=['GET'])
def get_currencies():
    user_id = session['user_id']
    di.init_currencies(user_id)
    return jsonify(response=Currency.serialize_list(Currency.all(user_id)))
