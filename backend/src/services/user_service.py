from models.user import User, db
from config.admin_list import admin_users
from flask import jsonify


def get_user_by_id(id: int):
    """Get a user by id.

    Args:
        id (int): id of the user.

    Returns:
        User or None: the user if there is one for the given id. If not, returns None.
    """
    user = User.query.filter_by(id=id).first()
    return user


def get_user_by_email(email: str):
    """Get a user by email.

    Args:
        email (str): email of the user.

    Returns:
        User or None: the user if there is one for the given email. If not, returns None.
    """
    user = User.query.filter_by(email=email).first()
    return user


def create_user(name: str, email: str, profile_pic_url: str) -> User:
    """Creates and adds a new user to the db.

    Args:
        name (str): name of the user.
        email (str): email of the user.
        profile_pic_url (str): profile picture url of the user.

    Returns:
        User: the new user.
    """
    # See if the email is part of the admin_users list
    is_admin = email in admin_users

    # Create new User object
    user = User(
        name=name,
        email=email,
        profile_pic_url=profile_pic_url,
        admin=is_admin,
    )

    # Add user to the db
    db.session.add(user)
    db.session.commit()

    return user


def update_name(id: int, new_name: str):
    """Update the name of an existing user.

    Args:
        id (int): id of the user to update.
        new_name (str): the new name for the user.

    Returns:
        JSON: JSON message about success or failure.
    """
    user = User.query.get(id)

    # If user is found with the given id
    if user:
        try:
            user.name = new_name
            db.session.commit()
            return (
                jsonify({'message': f"User's name updated successfully to: {new_name}"}),
                200,
            )
        # If there is a database error
        except Exception as e:
            db.session.rollback()
            return jsonify(
                {
                    'error': 'Error occurred while updating name in db.',
                    'details': str(e),
                }
            ), 500
    # If there is no user with the given id
    else:
        return jsonify(
            {'error': 'User with that id not found. Name not updated.'}
        ), 404
