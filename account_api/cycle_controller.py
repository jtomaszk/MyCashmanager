from flask import *

from common.common import *
from account_model.cycle import Cycle
from account_api.cycle_service import save_cycle_execution

__author__ = 'jtomaszk'

cycle_api = Blueprint('cycle_api', __name__)


@cycle_api.route('/cycles', methods=['GET'])
def get_cycles():
    user_id = session['user_id']
    return jsonify(response=Cycle.serialize_list(Cycle.all(user_id)))


@cycle_api.route('/cycle', methods=['PUT'])
def put_cycle():
    item = read_cycle_from_request()
    item.add()
    return '', 204


@cycle_api.route('/cycle', methods=['POST'])
def post_cycle():
    item = read_cycle_from_request()
    item.id = request.json['item']['id']
    item.update()
    return '', 200


@cycle_api.route('/cycle/<uuid:cycle_id>', methods=['DELETE'])
def delete_cycle(cycle_id):
    Cycle.get(cycle_id).delete()
    return jsonify(response=True)


def read_cycle_from_request():
    account_id = request.json['item']['account']['id']
    category_id = request.json['item']['category']['id']
    date_start = to_date(request.json['item']['date_start'])
    name = request.json['item']['name']
    repeat_type = request.json['item']['repeatType']['enum']
    repeat_every = request.json['item']['repeat_every']
    transaction_type = request.json['item']['type']['enum']
    amount = to_decimal(request.json['item']['amount'])
    max_count = request.json['item'].get('max_count', None)
    date_end = to_date(request.json['item'].get('date_end', None))

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
    return item


@cycle_api.route('/transaction/cycle/<uuid:cycle_id>', methods=['PUT'])
def put_cycle_transaction(cycle_id):
    amount = to_decimal(request.json['item']['value'])
    execution_date = to_date(request.json['item']['date'])
    save_cycle_execution(cycle_id, amount, execution_date)
    return '', 204



