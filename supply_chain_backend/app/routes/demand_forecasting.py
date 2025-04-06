from app import db , app
import uuid
from flask import request, jsonify, Blueprint
from app.utils.helpers import add_error_to_list


# start all routes with /forecast
forecast = Blueprint('forecast', __name__, url_prefix='/forecast')

@forecast.route('/demand', methods=['GET'])
def get_demand_forecast():
    return jsonify({'message': 'Get demand forecast'})

@forecast.route('/trends', methods=['GET'])
def get_trends():
    return jsonify({'message': 'Get trends'})

@forecast.route('/train', methods=['POST'])
def train_model():
    return jsonify({'message': 'Train model'})

@forecast.route('/model/status', methods=['GET'])
def get_model_status():
    return jsonify({'message': 'Get model status'})

@forecast.route('/refine', methods=['POST'])
def refine_model():
    return jsonify({'message': 'Refine model'})


