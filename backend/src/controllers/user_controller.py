from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.user_service import get_user_by_id, get_user_by_email, create_user, update_name
from models.user import User
from extensions import db
from services.user_service import get_user_by_id
# Create a Flask Blueprint for user-related routes
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Fetch a user by their ID."""
    user = get_user_by_id(user_id)
    if user:
        # Use to_dict for serialization
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@user_blueprint.route('/users/register', methods=['POST'])
def register_user():
    """Register a new user."""
    data = request.get_json()

    # Validate required fields
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required'}), 400

    # Check if a user with the same email already exists
    if get_user_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 409

    try:
        # Use the create_user service to add a new user
        new_user = create_user(
            name=data['name'],
            email=data['email'],
            profile_pic_url=data.get('profile_pic_url', ''),
            password=data['password']  # Raw password; will be hashed by the model
        )
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create user', 'details': str(e)}), 500


@user_blueprint.route('/users/login', methods=['POST'])
def login_user():
    """Login an existing user."""
    data = request.get_json()
    user = get_user_by_email(data['email'])

    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user_name(user_id):
    """Update a user's name by their ID."""
    data = request.get_json()

    # Validate input
    new_name = data.get('new_name')
    if not new_name:
        return jsonify({'error': 'New name is required'}), 400

    user = get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User with the specified ID not found.'}), 404

    try:
        # Update the user's name
        user.name = new_name
        db.session.commit()  # Ensure db is properly committed
        return jsonify({'message': f"User's name updated successfully to: {new_name}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user name', 'details': str(e)}), 500


@user_blueprint.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    """Fetch a user by their email."""
    user = get_user_by_email(email)

    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404
