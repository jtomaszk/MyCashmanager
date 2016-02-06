import datetime
import decimal
from flask import *

from account_model.cycle import Cycle
from account_api.cycle_service import save_cycle_execution

__author__ = 'jtomaszk'

cycle_api = Blueprint('cycle_api', __name__)


@cycle_api.route('/cycles', methods=['GET'])
def get_cycles():
    user_id = session['user_id']
    return jsonify(response=Cycle.serialize_list(Cycle.all(user_id)))


@cycle_api.route('/cycle', methods=['PUT'])
def put_cycles():
    account_id = request.json['item']['account']['id']
    category_id = request.json['item']['category']['id']
    date_start = request.json['item']['dateStart']
    date_start = datetime.datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    name = request.json['item']['name']
    repeat_type = request.json['item']['repeatType']['enum']
    repeat_every = request.json['item']['repeatValue']
    transaction_type = request.json['item']['type']['enum']
    amount = decimal.Decimal(request.json['item']['value'])
    if 'count' in request.json['item']:
        max_count = request.json['item']['count']
    else:
        max_count = None
    if 'dateEnd' in request.json['item'] and request.json['item']['dateEnd'] is not None:
        date_end = request.json['item']['dateEnd']
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        date_end = None

    item = Cycle(account_id,
                 name,
                 date_start,
                 repeat_type,
                 repeat_every,
                 amount,
                 category_id,
                 transaction_type,
                 max_count,
                 date_end)
    item.add()
    return '', 204


@cycle_api.route('/transaction/cycle/<uuid:cycle_id>', methods=['PUT'])
def put_cycle_transaction(cycle_id):
    amount = decimal.Decimal(request.json['item']['value'])
    execution_date = request.json['item']['date']
    execution_date = datetime.datetime.strptime(execution_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    save_cycle_execution(cycle_id, amount, execution_date)
    return '', 204
