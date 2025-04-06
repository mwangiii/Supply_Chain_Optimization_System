import uuid
from app import app, db
from flask import Blueprint, request, jsonify
from models.Users import User
from app.utils.helpers import add_error_to_list, generate_password_hash, generate_jwt_token

"""The users routes"""

# Create a Blueprint for authentication routes
auth = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/")
def index():
    return "Welcome to the supply chain management system api!"

@auth.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    errors_list = []

    if not data.get("firstName"):
        add_error_to_list(errors_list, "First name is required", 400)
    if not data.get("lastName"):
        add_error_to_list(errors_list, "Last name is required", 400)
    if not data.get("email"):
        add_error_to_list(errors_list, "Email is required", 400)
    if not data.get("password"):
        add_error_to_list(errors_list, "Password is required", 400)
    if User.query.filter_by(email=data.get("email")).first():
        add_error_to_list(errors_list, "Email already exists", 400)

    if errors_list:
        return jsonify({
            "status": "bad request",
            "message": "Some required fields are missing",
            "errors": errors_list
        }), 400    

    # Hash the password before saving it
    hashed_password = generate_password_hash(data['password'])  

    new_user = User(
        userid=uuid.uuid4().hex,
        firstName=data.get("firstName"),
        lastName=data.get("lastName"),
        email=data.get("email"),
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    jwt_token = generate_jwt_token(new_user.userid)
    return jsonify({
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "userid": new_user.userid,
            "firstName": new_user.firstName,
            "lastName": new_user.lastName,
            "email": new_user.email,
            "jwt_token": jwt_token
        }
    }), 201

@auth.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    errors_list = []

    if not data.get("email"):
        add_error_to_list(errors_list, "Email is required", 400)
    if not data.get("password"):
        add_error_to_list(errors_list, "Password is required", 400)

    if errors_list:
        return jsonify({
            "status": "bad request",
            "message": "Some required fields are missing",
            "errors": errors_list
        }), 400    

    user = User.query.filter_by(email=data.get("email")).first()
    if not user:
        return jsonify({
            "status": "bad request",
            "message": "User not found",
            "errors": errors_list
        }), 400

    if not bcrypt.check_password_hash(user.password, data.get("password")):
        return jsonify({
            "status": "bad request",
            "message": "Invalid password",
            "errors": errors_list
        }), 400

    return jsonify({
        "status": "success",
        "message": "User logged in successfully",
        "data": {
            "userid": user.userid,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        }
    }), 200

@auth.route("/profile", methods=["GET"])
def get_user_profile():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({
            "status": "bad request",
            "message": "Authorization header is required"
        }), 400

    jwt_token = auth_header.split(" ")[1]
    try:
        decoded_data = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({
            "status": "bad request",
            "message": "Token has expired"
        }), 400
    except jwt.InvalidTokenError:
        return jsonify({
            "status": "bad request",
            "message": "Invalid token"
        }), 400

    user = User.query.filter_by(userid=decoded_data.get("userid")).first()
    if not user:
        return jsonify({
            "status": "bad request",
            "message": "User not found"
        }), 400

    return jsonify({
        "status": "success",
        "message": "User profile retrieved successfully",
        "data": {
            "userid": user.userid,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        }
    }), 200

@auth.route("/profile", methods=["PUT"])
def update_user_profile():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({
            "status": "bad request",
            "message": "Authorization header is required"
        }), 400

    jwt_token = auth_header.split(" ")[1]
    try:
        decoded_data = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({
            "status": "bad request",
            "message": "Token has expired"
        }), 400
    except jwt.InvalidTokenError:
        return jsonify({
            "status": "bad request",
            "message": "Invalid token"
        }), 400

    user = User.query.filter_by(userid=decoded_data.get("userid")).first()
    if not user:
        return jsonify({
            "status": "bad request",
            "message": "User not found"
        }), 400

    data = request.get_json()
    errors_list = []

    if not data.get("firstName"):
        add_error_to_list(errors_list, "First name is required", 400)
    if not data.get("lastName"):
        add_error_to_list(errors_list, "Last name is required", 400)
    if not data.get("email"):
        add_error_to_list(errors_list, "Email is required", 400)

    if errors_list:
        return jsonify({
            "status": "bad request",
            "message": "Some required fields are missing",
            "errors": errors_list
        }), 400    

    user.firstName = data.get("firstName")
    user.lastName = data.get("lastName")
    user.email = data.get("email")
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User profile updated successfully",
        "data": {
            "userid": user.userid,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email
        }
    }), 200

@auth.route("/password/change", methods=["PUT"])
def change_user_password():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({
            "status": "bad request",
            "message": "Authorization header is required"
        }), 400

    jwt_token = auth_header.split(" ")[1]
    try:
        decoded_data = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({
            "status": "bad request",
            "message": "Token has expired"
        }), 400
    except jwt.InvalidTokenError:
        return jsonify({
            "status": "bad request",
            "message": "Invalid token"
        }), 400

    user = User.query.filter_by(userid=decoded_data.get("userid")).first()
    if not user:
        return jsonify({
            "status": "bad request",
            "message": "User not found"
        }), 400

    data = request.get_json()
    errors_list = []

    if not data.get("oldPassword"):
        add_error_to_list(errors_list, "Old password is required", 400)
    if not data.get("newPassword"):
        add_error_to_list(errors_list, "New password is required", 400)

    if errors_list:
        return jsonify({
            "status": "bad request",
            "message": "Some required fields are missing",
            "errors": errors_list
        }), 400    

    if not bcrypt.check_password_hash(user.password, data.get("oldPassword")):
        return jsonify({
            "status": "bad request",
            "message": "Invalid old password",
            "errors": errors_list
        }), 400

    user.password = generate_password_hash(data.get("newPassword"))
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User password changed successfully"
    }), 200

# Register the Blueprint with the Flask application
app.register_blueprint(auth)


