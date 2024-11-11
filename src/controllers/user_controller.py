from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.user_service import get_user_by_id, get_user_by_email, create_user, update_name
from models.user import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@user_blueprint.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if get_user_by_email(data['email']):
        return jsonify({'message': 'Email already exists'}), 409
    hashed_password = generate_password_hash(data['password'])
    try:
        new_user = create_user(
            name=data['name'],
            email=data['email'],
            profile_pic_url=data.get('profile_pic_url', ''),
            password=hashed_password
        )
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create user', 'details': str(e)}), 500

@user_blueprint.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = get_user_by_email(data['email'])
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'user': user.serialize()}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user_name(user_id):
    data = request.get_json()
    response = update_name(user_id, data['new_name'])
    return response

@user_blueprint.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    user = get_user_by_email(email)
    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({'message': 'User not found'}), 404
