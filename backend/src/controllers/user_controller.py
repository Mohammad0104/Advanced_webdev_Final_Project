from flask import Blueprint, request, jsonify
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

    try:
        # Create user without the password field, since we don't handle passwords
        new_user = create_user(
            name=data['name'],
            email=data['email'],
            profile_pic_url=data.get('profile_pic_url', '')
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
    
    # Retrieve the user by email (no password check)
    user = get_user_by_email(data['email'])
    
    if user:
        # If user is found, return the user details
        return jsonify({'message': 'Login successful', 'user': user.serialize()}), 200
    else:
        # If the login fails (no user found), return an invalid credentials message
        return jsonify({'message': 'Invalid email'}), 401

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
        return jsonify(user.to_dict()), 200
    else:
        # If no user is found, return an error message with a 404 NOT FOUND status
        return jsonify({'message': 'User not found'}), 404
