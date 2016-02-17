from flask import Blueprint, request, jsonify
from flask.ext.login import current_user

from account_model.category import Category
from account_model.transaction import Transaction
from account_api.data_initializer import DataInitializer
from auth_api.auth_controller import login_required

__author__ = 'jtomaszk'

category_api = Blueprint('category_api', __name__)

di = DataInitializer()


@category_api.route('/categories', methods=['GET'])
@login_required
def get_categories():
    user_id = current_user.id
    di.init_categories(user_id)
    return jsonify(response=Category.serialize_list(Category.all(user_id)))


@category_api.route('/category', methods=['PUT'])
@login_required
def put_category():
    user_id = current_user.id
    name = request.json['category']['name']
    category = Category(name, user_id)
    ret = category.add()
    return jsonify(response=ret.serialize())


@category_api.route('/category', methods=['POST'])
@login_required
def post_category():
    user_id = current_user.id
    name = request.json['category']['name']
    cat_id = request.json['category']['id']
    category = Category(name, user_id)
    category.id = cat_id
    ret = category.update()
    return jsonify(response=ret.serialize())


@category_api.route('/category/<uuid:category_id>', methods=['DELETE'])
def delete_category(category_id):
    trans_list = Transaction.query.filter_by(category_id=category_id).all()
    if len(trans_list) > 0:
        return 'Category is connected to some transactions', 400

    Category.get(category_id).delete()
    return jsonify(response=True)
