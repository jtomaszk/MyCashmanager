from flask import *

from common.common import *
from account_model.account import *
from account_api.data_initializer import DataInitializer

__author__ = 'jtomaszk'

transaction_api = Blueprint('transaction_api', __name__)

di = DataInitializer()


@transaction_api.route('/transaction', methods=['PUT'])
def put_transaction():
    account_id = request.json['accountId']
    value = to_decimal(request.json['value'])
    trans_type = request.json['type']
    category_id = request.json['categoryId']
    comment = request.json.get('comment', '')
    trans_date = to_date(request.json['date'])

    account = Account.get(account_id)

    if trans_type == 'INCOME':
        trans = account.add_income(value, category_id, comment)
        trans.date = trans_date
    elif trans_type == 'OUTCOME':
        trans = account.add_outcome(value, category_id, comment)
        trans.date = trans_date
    elif trans_type == 'TRANSFER':
        destination_account_id = request.json['destinationAccountId']
        destination_account = Account.get(destination_account_id)
        source = account.add_outcome(value, category_id, comment)
        source.date = trans_date
        destination = destination_account.add_income(value, category_id, comment)
        destination.date = trans_date
        source.connect(destination)
        destination.connect(source)
    else:
        return 'invalid type', 400

    return '', 204


@transaction_api.route('/transaction', methods=['POST'])
def post_transaction():
    transaction_id = request.json['id']
    new_value = to_decimal(request.json['value'])
    new_trans_type = request.json['type']
    category_id = request.json['category_id']
    comment = request.json.get('comment', '')
    trans_date = to_date(request.json['date'])

    transaction = Transaction.get(transaction_id)
    account = Account.get(transaction.account_id)

    old_trans_type = transaction.transaction_type
    old_value = transaction.amount

    if old_trans_type == 'INCOME':
        account.decrease_balance(old_value)
    elif old_trans_type == 'OUTCOME':
        account.increase_balance(old_value)
    else:
        return 'invalid type', 400

    if new_trans_type == 'INCOME':
        account.increase_balance(new_value)
    elif new_trans_type == 'OUTCOME':
        account.decrease_balance(new_value)
    else:
        return 'invalid type', 400

    transaction.transaction_type = new_trans_type
    transaction.amount = new_value
    transaction.comment = comment
    transaction.category_id = category_id
    transaction.date = trans_date

    return '', 200


@transaction_api.route('/transaction/<uuid:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.get(transaction_id)
    account = Account.get(transaction.account_id)

    old_trans_type = transaction.transaction_type
    old_value = transaction.amount

    if old_trans_type == 'INCOME':
        account.decrease_balance(old_value)
    elif old_trans_type == 'OUTCOME':
        account.increase_balance(old_value)
    else:
        return 'invalid type', 400

    if transaction.transfer_id is not None:
        dest_trans = Transaction.get(transaction.transfer_id)
        dest_account = Account.get(dest_trans.account_id)

        if old_trans_type == 'INCOME':
            dest_account.increase_balance(old_value)
        elif old_trans_type == 'OUTCOME':
            dest_account.decrease_balance(old_value)

        dest_trans.delete()

    transaction.delete()

    return jsonify(response=True)


@transaction_api.route('/transaction/<uuid:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    return jsonify(response=Transaction.get(transaction_id).serialize())


@transaction_api.route('/transactions/<uuid:account_id>', methods=['GET'])
def get_transactions(account_id):
    account = Account.get(account_id)
    return jsonify(response=Transaction.serialize_list(account.transactions),
                   account=account.serialize())
