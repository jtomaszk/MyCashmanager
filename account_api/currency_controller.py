from flask import Blueprint, jsonify
from flask.ext.login import current_user

from account_model.currency import Currency
from account_api.data_initializer import DataInitializer
from auth_api.auth_controller import login_required

__author__ = 'jtomaszk'

currency_api = Blueprint('currency_api', __name__)

di = DataInitializer()

@login_required
@currency_api.route('/currencies', methods=['GET'])
def get_currencies():
    user_id = current_user.id
    di.init_currencies(user_id)
    return jsonify(response=Currency.serialize_list(Currency.all(user_id)))
