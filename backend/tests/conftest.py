import pytest
import sys
import os

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.app import create_app
from src.models import db
from config.config import TestingConfig  # Import TestingConfig for testing environment


@pytest.fixture(scope="module")
def test_client():
    """
    Fixture to set up the test client for the Flask application.
    """
    # Create the Flask app with TestingConfig
    app = create_app(TestingConfig)

    # Initialize the app context and database
    with app.app_context():
       
        db.create_all()  # Create all tables for the test database
    
    # Provide the test client
    with app.test_client() as client:
        yield client

    # Cleanup after tests
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="function")
def add_user():
    """
    Fixture to add a sample user to the database for testing.
    """
    from src.models.user import User

    def _add_user(name, email, profile_pic_url, admin=False):
        user = User(
            name=name,
            email=email,
            profile_pic_url=profile_pic_url,
            admin=admin
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to add user: {e}")
    return _add_user


@pytest.fixture(scope="function")
def clear_db():
    """
    Fixture to clear all tables in the database after a test function.
    """
    yield  # Run the test
    with db.session.no_autoflush:  # Prevent auto-flush during teardown
        db.session.remove()
        db.drop_all()  # Drop all tables after the test
        db.create_all()  # Recreate the tables for the next test
