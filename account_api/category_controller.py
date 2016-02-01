from flask import *

from account_model.category import Category
from account_api.data_initializer import DataInitializer

__author__ = 'jtomaszk'

category_api = Blueprint('category_api', __name__)

di = DataInitializer()


@category_api.route('/categories', methods=['GET'])
def get_categories():
    user_id = session['user_id']
    di.init_categories(user_id)
    return jsonify(response=Category.serialize_list(Category.all(user_id)))


@category_api.route('/category', methods=['PUT'])
def put_category():
    user_id = session['user_id']
    name = request.json['category']['name']
    category = Category(name, user_id)
    ret = category.add()
    return jsonify(response=ret.serialize())


@category_api.route('/category', methods=['POST'])
def post_category():
    user_id = session['user_id']
    name = request.json['category']['name']
    cat_id = request.json['category']['id']
    category = Category(name, user_id)
    category.id = cat_id
    ret = category.update()
    return jsonify(response=ret.serialize())

