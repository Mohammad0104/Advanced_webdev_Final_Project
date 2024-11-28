from models.user import User, db
from config.admin_list import admin_users
from flask import jsonify


def get_user_by_id(user_id: int):
    """Get a user by ID.

    Args:
        user_id (int): ID of the user.

    Returns:
        User or None: The user object if found, otherwise None.
    """
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email: str):
    """Get a user by email.

    Args:
        email (str): Email of the user.

    Returns:
        User or None: The user object if found, otherwise None.
    """
    return User.query.filter_by(email=email).first()


def create_user(name: str, email: str, profile_pic_url: str) -> User:
    """Creates and adds a new user to the database.

    Args:
        name (str): Name of the user.
        email (str): Email of the user.
        profile_pic_url (str): Profile picture URL of the user.

    Returns:
        User: The newly created user object.
    """
    is_admin = email in admin_users
    user = User(
        name=name,
        email=email,
        profile_pic_url=profile_pic_url,
        admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    return user


def update_name(user_id: int, new_name: str):
    """Update the name of an existing user.

    Args:
        user_id (int): ID of the user to update.
        new_name (str): The new name for the user.

    Returns:
        JSON: JSON message about success or failure.
    """
    user = User.query.get(user_id)
    if user:
        try:
            user.name = new_name
            db.session.commit()
            return jsonify(
                {'message': f"User's name updated successfully to: {new_name}"}
            ), 200
        except Exception as e:
            db.session.rollback()
            return jsonify(
                {'error': 'Error occurred while updating name in db.',
                 'details': str(e)}
            ), 500
    return jsonify({'error': 'User with that ID not found. Name not updated.'}), 404
