from app import db, app
from flask import Blueprint, request, jsonify
from app.models import DataCollection
import uuid
from app.utils.helpers import add_error_to_list

# Create a Blueprint for data routes
data = Blueprint('data', __name__, url_prefix='/data')

@data.route("/upload", methods=["POST"])
def upload_data():
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

    new_data = DataCollection(
        dataid=uuid.uuid4().hex,
        title=data.get("title"),
        description=data.get("description"),
        data=data.get("data")
    )
    db.session.add(new_data)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Data uploaded successfully",
        "data": {
            "dataid": new_data.dataid,
            "title": new_data.title,
            "description": new_data.description,
            "data": new_data.data
        }
    }), 201

@data.route("/", methods=["GET"])
def get_all_data():
    data = DataCollection.query.all()
    data_list = []

    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })

    return jsonify({
        "status": "success",
        "data": data_list
    }), 200

@data.route("/<dataid>", methods=["GET"])
def get_data(dataid):
    data = DataCollection.query.filter_by(dataid=dataid).first()
    if not data:
        return jsonify({
            "status": "not found",
            "message": "Data not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": {
            "dataid": data.dataid,
            "title": data.title,
            "description": data.description,
            "data": data.data
        }
    }), 200

@data.route("/status", methods=["GET"])
def get_data_status():
    data = DataCollection.query.all()
    data_list = []

    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })

    return jsonify({
        "status": "success",
        "data": data_list
    }), 200

@data.route("/inventory", methods=["GET"])
def get_data_inventory():
    data = DataCollection.query.all()
    data_list = []

    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })

    return jsonify({
        "status": "success",
        "data": data_list
    }), 200

@data.route("/sales", methods=["GET"])
def get_data_sales():
    data = DataCollection.query.all()
    data_list = []

    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })

    return jsonify({
        "status": "success",
        "data": data_list
    }), 200

@data.route("/logistics", methods=["GET"])
def get_data_logistics():
    data = DataCollection.query.all()
    data_list = []

    for item in data:
        data_list.append({
            "dataid": item.dataid,
            "title": item.title,
            "description": item.description,
            "data": item.data
        })

    return jsonify({
        "status": "success",
        "data": data_list
    }), 200

@data.route("/clear", methods=["DELETE"])
def clear_data():
    data = DataCollection.query.all()
    for item in data:
        db.session.delete(item)
        db.session.commit()

    return jsonify({
        "status": "success",
        "message": "All data cleared"
    }), 200

# Register the Blueprint with the Flask application
app.register_blueprint(data)

