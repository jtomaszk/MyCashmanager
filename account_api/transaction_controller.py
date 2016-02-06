from flask import *

from account_model.account import *
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
    elif trans_type == 'TRANSFER':
        destination_account_id = request.json['destinationAccountId']
        destination_account = Account.get_account(destination_account_id, user_id)
        source = account.add_outcome(value, category_id, comment)
        destination = destination_account.add_income(value, category_id, comment)
        source.connect(destination)
        destination.connect(source)
    else:
        return '', 400

    return '', 204


@transaction_api.route('/transaction', methods=['POST'])
def post_transaction():
    # TODO
    raise Exception('Not implemented!')


@transaction_api.route('/transaction/<uuid:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    # TODO
    raise Exception('Not implemented!')


@transaction_api.route('/transaction/<uuid:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    # TODO
    raise Exception('Not implemented!')


@transaction_api.route('/transactions/<uuid:account_id>', methods=['GET'])
def get_transactions(account_id):
    user_id = session['user_id']
    account = Account.get_account(account_id, user_id)
    return jsonify(response=Transaction.serialize_list(account.transactions),
                   account=account.serialize())
