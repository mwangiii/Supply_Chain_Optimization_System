import jwt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

JWT_SECRET_KEY = '4f8b31dc8ee3437486e3424bcb2d6f0b'  # Keep this in config instead!

# Function for adding errors to a list
def add_error_to_list(errors_list, message, status_code):
    errors_list.append({"message": message, "status_code": status_code})

# Function for generating password hash
def generate_password_hash(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")

# Function for generating JWT token
def generate_jwt_token(userid):
    return jwt.encode({"userid": userid}, JWT_SECRET_KEY, algorithm="HS256")

