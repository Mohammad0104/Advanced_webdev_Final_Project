from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.user_service import get_user_by_id, get_user_by_email, create_user, update_name
from models.user import User

# Create a Flask Blueprint named 'user'. This modularizes the routes related to user operations.
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Fetch a user by their ID
    user = get_user_by_id(user_id)
    if user:
        # If the user is found, serialize their data and return it with a 200 OK status
        return jsonify(user.serialize()), 200
    else:
        # If the user is not found, return an error message with a 404 NOT FOUND status
        return jsonify({'message': 'User not found'}), 404

@user_blueprint.route('/users/register', methods=['POST'])
def register_user():
    # Extract data from the incoming request
    data = request.get_json()
    # Check if a user with the same email already exists
    if get_user_by_email(data['email']):
        return jsonify({'message': 'Email already exists'}), 409
    # Generate a hashed password for security
    hashed_password = generate_password_hash(data['password'])
    try:
        # Attempt to create a new user with the provided data
        new_user = create_user(
            name=data['name'],
            email=data['email'],
            profile_pic_url=data.get('profile_pic_url', ''),
            password=hashed_password
        )
        # If successful, serialize the new user's data and return it with a 201 CREATED status
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        # If an error occurs, return an error message with a 500 INTERNAL SERVER ERROR status
        return jsonify({'error': 'Failed to create user', 'details': str(e)}), 500

@user_blueprint.route('/users/login', methods=['POST'])
def login_user():
    # Extract data from the incoming request
    data = request.get_json()
    # Retrieve the user by email
    user = get_user_by_email(data['email'])
    # Check if the user exists and the password matches
    if user and check_password_hash(user.password, data['password']):
        # If successful, serialize the user's data and return it with a message
        return jsonify({'message': 'Login successful', 'user': user.serialize()}), 200
    else:
        # If the login fails, return an invalid credentials message with a 401 UNAUTHORIZED status
        return jsonify({'message': 'Invalid email or password'}), 401

@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user_name(user_id):
    # Extract new name from the request data
    data = request.get_json()
    # Call the service to update the user's name
    response = update_name(user_id, data['new_name'])
    return response

@user_blueprint.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    # Fetch a user by their email
    user = get_user_by_email(email)
    if user:
        # If the user is found, serialize their data and return it with a 200 OK status
        return jsonify(user.serialize()), 200
    else:
        # If no user is found, return an error message with a 404 NOT FOUND status
        return jsonify({'message': 'User not found'}), 404