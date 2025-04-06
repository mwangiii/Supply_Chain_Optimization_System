from app import db , app
import uuid
from flask import request, jsonify, Blueprint
from app.utils.helpers import add_error_to_list


tracking = Blueprint('tracking', __name__, url_prefix='/tracking')

@tracking.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({'message': 'Get orders'})

@tracking.route('/order/<id>', methods=['GET'])
def get_order(id):
    return jsonify({'message': 'Get order'})

@tracking.route('/update', methods=['POST'])
def update_order():
    return jsonify({'message': 'Update order'})

@tracking.route('/delays', methods=['GET'])
def get_delays():
    return jsonify({'message': 'Get delays'})

@tracking.route('/eta', methods=['GET'])
def get_eta():
    return jsonify({'message': 'Get eta'})
