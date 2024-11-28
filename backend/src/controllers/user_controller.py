from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.user_service import get_user_by_id, get_user_by_email, create_user, update_name
from models.user import User

# Create a Flask Blueprint named 'user'. This modularizes the routes related to user operations.
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """Endpoint to get the user by id

    Args:
        user_id (int): the id of the user to get

    Returns:
        JSON: JSON message with the user or error message
    """
    # Fetch a user by their ID
    user = get_user_by_id(user_id)
    if user:
        # If the user is found, serialize their data and return it with a 200 OK status
        return jsonify(user.serialize()), 200
    else:
        # If the user is not found, return an error message with a 404 NOT FOUND status
        return jsonify({'message': 'User not found'}), 404



@user_blueprint.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    """_summary_

    Args:
        email (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Fetch a user by their email
    user = get_user_by_email(email)

    if user:
        # If the user is found, serialize their data and return it with a 200 OK status
        return jsonify(user.to_dict()), 200
    else:
        # If no user is found, return an error message with a 404 NOT FOUND status
        return jsonify({'message': 'User not found'}), 404