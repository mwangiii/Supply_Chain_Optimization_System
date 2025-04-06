from app import db , app
import uuid
from flask import request, jsonify, Blueprint
from app.utils.helpers import add_error_to_list


# GET /suppliers
# POST /suppliers
# GET /suppliers/{id}
# PUT /suppliers/{id}
# DELETE /suppliers/{id}
# GET /inventory/items
# POST /inventory/items
# GET /inventory/items/{id}
# PUT /inventory/items/{id}
# DELETE /inventory/items/{id}
# GET /inventory/stock-levels
# POST /inventory/restock

suppliers = Blueprint('suppliers', __name__, url_prefix='/suppliers')

@suppliers.route('', methods=['GET'])
def get_suppliers():
    return jsonify({'message': 'Get suppliers'})

@suppliers.route('', methods=['POST'])
def create_supplier():
    return jsonify({'message': 'Create supplier'})

@suppliers.route('/<id>', methods=['GET'])
def get_supplier(id):
    return jsonify({'message': 'Get supplier'})

@suppliers.route('/<id>', methods=['PUT'])
def update_supplier(id):
    return jsonify({'message': 'Update supplier'})

@suppliers.route('/<id>', methods=['DELETE'])
def delete_supplier(id):
    return jsonify({'message': 'Delete supplier'})

@suppliers.route('/inventory/items', methods=['GET'])
def get_items():
    return jsonify({'message': 'Get items'})

@suppliers.route('/inventory/items', methods=['POST'])
def create_item():
    return jsonify({'message': 'Create item'})


@suppliers.route('/inventory/items/<id>', methods=['GET'])
def get_item(id):
    return jsonify({'message': 'Get item'})

@suppliers.route('/inventory/items/<id>', methods=['PUT'])
def update_item(id):
    return jsonify({'message': 'Update item'})

@suppliers.route('/inventory/items/<id>', methods=['DELETE'])
def delete_item(id):
    return jsonify({'message': 'Delete item'})

@suppliers.route('/inventory/stock-levels', methods=['GET'])
def get_stock_levels():
    return jsonify({'message': 'Get stock levels'})

@suppliers.route('/inventory/restock', methods=['POST'])
def restock():
    return jsonify({'message': 'Restock'})
