from models.user import User, db
from config.admin_list import admin_users
from flask import jsonify
from werkzeug.security import generate_password_hash
from extensions import db
from models.user import User
def get_user_by_id(id: int):
    """Get a user by id.

    Args:
        id (int): ID of the user.

    Returns:
        User or None: The user if found, or None if not found.
    """
    return User.query.filter_by(id=id).first()

def get_user_by_email(email: str):
    """Get a user by email.

    Args:
        email (str): Email of the user.

    Returns:
        User or None: The user if found, or None if not found.
    """
    return User.query.filter_by(email=email).first()

def create_user(name: str, email: str, profile_pic_url: str, password: str) -> User:
    """Create and add a new user to the database."""
    try:
        is_admin = email in admin_users
        user = User(
            name=name,
            email=email,
            profile_pic_url=profile_pic_url,
            admin=is_admin
        )
        user.password = password  # Set the raw password; it will be hashed
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating user: {str(e)}")

def update_name(id: int, new_name: str):
    """Update a user's name."""
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User with the specified ID not found.'}), 404

    try:
        user.name = new_name
        db.session.commit()  # Ensure db is imported and properly committed
        return jsonify({'message': f"User's name updated successfully to: {new_name}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user name', 'details': str(e)}), 500


def delete_user(id: int):
    """Delete a user by ID.

    Args:
        id (int): ID of the user to delete.

    Returns:
        JSON: JSON message about success or failure.
    """
    user = get_user_by_id(id)

    if not user:
        # Return 404 if the user is not found
        return jsonify({'error': 'User with that ID not found. User not deleted.'}), 404

    try:
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f"User with ID {id} successfully deleted."}), 200
    except Exception as e:
        # Handle database errors
        db.session.rollback()
        return jsonify({'error': 'Error occurred while deleting user from the database.',
                        'details': str(e)}), 500

def update_password(id: int, new_password: str):
    """Update the password of an existing user.

    Args:
        id (int): ID of the user to update.
        new_password (str): The new password to set.

    Returns:
        JSON: JSON message about success or failure.
    """
    user = get_user_by_id(id)

    if not user:
        # Return 404 if the user is not found
        return jsonify({'error': 'User with that ID not found. Password not updated.'}), 404

    try:
        # Hash the new password and update the user's record
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Password updated successfully.'}), 200
    except Exception as e:
        # Handle database errors
        db.session.rollback()
        return jsonify({'error': 'Error occurred while updating password in the database.',
                        'details': str(e)}), 500
