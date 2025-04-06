from app import db , app
import uuid
from flask import request, jsonify, Blueprint
from app.utils.helpers import add_error_to_list


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/overview', methods=['GET'])
def get_overview():
    return jsonify({'message': 'Get overview'})

@dashboard.route('/sales', methods=['GET'])
def get_sales():
    return jsonify({'message': 'Get sales'})

@dashboard.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify({'message': 'Get inventory'})

@dashboard.route('/logistics', methods=['GET'])
def get_logistics():
    return jsonify({'message': 'Get logistics'})

@dashboard.route('/reports', methods=['GET'])
def get_reports():
    return jsonify({'message': 'Get reports'})
