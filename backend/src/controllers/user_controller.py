from flask import Blueprint, jsonify
from services.user_service import get_user_by_id, get_user_by_email

# Create a Flask Blueprint named 'user'. This modularizes the routes related to user operations.
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """Endpoint to get the user by id.

    Args:
        user_id (int): the id of the user to get.

    Returns:
        JSON: JSON message with the user or error message.
    """
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user.serialize()), 200
    return jsonify({'message': 'User not found'}), 404


@user_blueprint.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    """Fetch a user by their email.

    Args:
        email (str): Email of the user to fetch.

    Returns:
        JSON: Serialized user data or error message.
    """
    user = get_user_by_email(email)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404
