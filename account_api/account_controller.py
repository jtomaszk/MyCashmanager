from flask import *

from account_model.account import *
from account_api.data_initializer import DataInitializer

__author__ = 'jtomaszk'

account_api = Blueprint('account_api', __name__)

di = DataInitializer()


@account_api.route('/accounts', methods=['GET'])
def get_accounts():
    user_id = session['user_id']
    accounts = Account.all(user_id)
    dict_account = Account.serialize_list(accounts)
    return jsonify(response=dict_account)


@account_api.route('/account', methods=['PUT'])
def put_account():
    user_id = session['user_id']
    currency_id = request.json['currencyId']
    account_name = request.json['accountName']
    Account(user_id, currency_id, account_name).add()
    return '', 204

