import pytest
import sys
import os
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import create_app
from extensions import db
from models.user import User

@pytest.fixture(scope="module")
def app():
    """Fixture to create a Flask app instance for testing."""
    app = create_app("config.config.TestingConfig")

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def test_client(app):
    """Fixture to set up the test client for the Flask application."""
    return app.test_client()


@pytest.fixture(scope="function")
def add_user(app):
    """Fixture to add a sample user to the database for testing."""
    def _add_user(name, email, profile_pic_url, admin=False, password="defaultpassword"):
        with app.app_context():
            user = User(
                name=name,
                email=email,
                profile_pic_url=profile_pic_url,
                admin=admin
            )
            user.password = password  # Use the password setter
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            return user
    return _add_user


@pytest.fixture(scope="function")
def clear_db(app):
    """Fixture to clear all tables in the database after a test function."""
    yield  # Run the test first
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
