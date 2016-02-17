from flask import Blueprint, request, jsonify
from flask.ext.login import current_user

from account_model.account import *
from account_api.data_initializer import DataInitializer
from auth_api.auth_controller import login_required


__author__ = 'jtomaszk'

account_api = Blueprint('account_api', __name__)

di = DataInitializer()


@account_api.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    user_id = current_user.id
    accounts = Account.all(user_id)
    dict_account = Account.serialize_list(accounts)
    return jsonify(response=dict_account)


@account_api.route('/account', methods=['PUT'])
@login_required
def put_account():
    user_id = current_user.id
    currency_id = request.json['currencyId']
    account_name = request.json['accountName']
    Account(user_id, currency_id, account_name).add()
    return '', 204
