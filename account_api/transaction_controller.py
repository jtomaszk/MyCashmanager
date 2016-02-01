from flask import *

from account_model.account import *
from account_model.category import Category
from account_model.currency import Currency
from account_api.data_initializer import DataInitializer

__author__ = 'jtomaszk'

transaction_api = Blueprint('transaction_api', __name__)

di = DataInitializer()


@transaction_api.route('/transaction', methods=['PUT'])
def put_transaction():
    user_id = session['user_id']
    account_id = request.json['accountId']
    value = request.json['value']
    trans_type = request.json['type']
    category_id = request.json['categoryId']
    if 'comment' in request.json:
        comment = request.json['comment']
    else:
        comment = None

    account = Account.get_account(account_id, user_id)

    if trans_type == 'INCOME':
        account.add_income(value, category_id, comment)
    elif trans_type == 'OUTCOME':
        account.add_outcome(value, category_id, comment)
    else:
        return '', 400

    return '', 204


@transaction_api.route('/transactions/<int:account_id>', methods=['GET'])
def get_transactions(account_id):
    user_id = session['user_id']
    account = Account.get_account(account_id, user_id)
    return jsonify(response=Transaction.serialize_list(account.transactions),
                   account=account.serialize())
