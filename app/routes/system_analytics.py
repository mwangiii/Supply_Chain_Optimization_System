from app import db, app
from flask import Blueprint, request, jsonify
from app.models import DataCollection
import uuid
from app.utils.helpers import add_error_to_list

# GET /ai/models
# POST /ai/models/train
# GET /ai/models/{id}/status
# GET /ai/models/{id}/performance
# POST /ai/models/{id}/retrain
# DELETE /ai/models/{id}

system_analytics = Blueprint('system_analytics', __name__, url_prefix='/ai/models')


@system_analytics.route("/", methods=["GET"])
def get_all_models():
    models = DataCollection.query.all()
    models_list = []

    for model in models:
        models_list.append({
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        })

    return jsonify({
        "status": "success",
        "data": models_list
    }), 200


@system_analytics.route("/train", methods=["POST"])
def train_model():
    data = request.get_json()
    errors_list = []

    if not data.get("title"):
        add_error_to_list(errors_list, "Title is required", 400)
    if not data.get("description"):
        add_error_to_list(errors_list, "Description is required", 400)
    if not data.get("data"):
        add_error_to_list(errors_list, "Data is required", 400)

    if errors_list:
        return jsonify({
            "status": "bad request",
            "message": "Some required fields are missing",
            "errors": errors_list
        }), 400

    new_model = DataCollection(
        dataid=uuid.uuid4().hex,
        title=data.get("title"),
        description=data.get("description"),
        data=data.get("data")
    )
    db.session.add(new_model)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Model trained successfully",
        "data": {
            "dataid": new_model.dataid,
            "title": new_model.title,
            "description": new_model.description,
            "data": new_model.data
        }
    }), 201


@system_analytics.route("/<dataid>/status", methods=["GET"])
def get_model_status(dataid):
    model = DataCollection.query.filter_by(dataid=dataid).first()

    if not model:
        return jsonify({
            "status": "not found",
            "message": "Model not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        }
    }), 200


@system_analytics.route("/<dataid>/performance", methods=["GET"])
def get_model_performance(dataid):
    model = DataCollection.query.filter_by(dataid=dataid).first()

    if not model:
        return jsonify({
            "status": "not found",
            "message": "Model not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        }
    }), 200


@system_analytics.route("/<dataid>/retrain", methods=["POST"])
def retrain_model(dataid):
    model = DataCollection.query.filter_by(dataid=dataid).first()

    if not model:
        return jsonify({
            "status": "not found",
            "message": "Model not found"
        }), 404

    return jsonify({
        "status": "success",
        "message": "Model retrained successfully",
        "data": {
            "dataid": model.dataid,
            "title": model.title,
            "description": model.description,
            "data": model.data
        }
    }), 200


@system_analytics.route("/<dataid>", methods=["DELETE"])
def delete_model(dataid):
    model = DataCollection.query.filter_by(dataid=dataid).first()

    if not model:
        return jsonify({
            "status": "not found",
            "message": "Model not found"
        }), 404

    db.session.delete(model)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Model deleted successfully"
    }), 200




