import pytest
from flask import Flask
from models import db
from models.user import User
from controllers.user_controller import user_blueprint
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    """Fixture to create a Flask application for testing."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    # Register the user blueprint
    app.register_blueprint(user_blueprint)

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    """Fixture to create a test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Add a sample user to the database."""
    user = User(
        name='Test User',
        email='test@example.com',
        profile_pic_url='https://example.com/profile.jpg',
        admin=False,
    )

    # Mock the serialize method for the sample user
    def mock_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile_pic_url': self.profile_pic_url,
            'admin': self.admin,
        }

    setattr(User, "serialize", mock_serialize)

    with app.app_context():
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user


def test_get_user(client, sample_user):
    """Test fetching a user by ID."""
    response = client.get(f'/users/{sample_user.id}')
    assert response.status_code == 200, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['id'] == sample_user.id
    assert data['name'] == sample_user.name
    assert data['email'] == sample_user.email
    assert data['profile_pic_url'] == sample_user.profile_pic_url


def test_get_user_not_found(client):
    """Test fetching a non-existent user by ID."""
    response = client.get('/users/999')
    assert response.status_code == 404, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['message'] == 'User not found'


def test_get_user_by_email(client, sample_user):
    """Test fetching a user by email."""
    response = client.get(f'/users/email/{sample_user.email}')
    assert response.status_code == 200, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['email'] == sample_user.email
    assert data['name'] == sample_user.name
    assert data['profile_pic_url'] == sample_user.profile_pic_url


