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

    # Attach mock_serialize method to the user instance
    setattr(User, "serialize", mock_serialize)

    with app.app_context():
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user


def test_register_user(client):
    """Test registering a new user."""
    payload = {
        'name': 'New User',
        'email': 'newuser@example.com',
        'profile_pic_url': 'https://example.com/profile_new.jpg',
    }

    # Mock the user creation process
    with patch("src.services.user_service.create_user") as mock_create_user:
        # Create a MagicMock object for the user
        mock_user = MagicMock()

        # Mock the `serialize` method of the mock user
        mock_user.serialize.return_value = {
            'id': 1,
            'name': payload['name'],
            'email': payload['email'],
            'profile_pic_url': payload['profile_pic_url'],
            'admin': False,
        }

        mock_create_user.return_value = mock_user

        response = client.post('/users/register', json=payload)

    assert response.status_code == 201, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['name'] == payload['name']
    assert data['email'] == payload['email']


def test_login_user(client, sample_user):
    """Test logging in a user."""
    payload = {
        'email': sample_user.email,
        # No password needed for OAuth
    }

    # Mock the login-related operations
    with patch("src.controllers.user_controller.get_user_by_email") as mock_get_user:
        # Mock the user object with the serialize method
        mock_user = MagicMock()
        mock_user.serialize.return_value = {
            'id': sample_user.id,
            'name': sample_user.name,
            'email': sample_user.email,
            'profile_pic_url': sample_user.profile_pic_url,
            'admin': sample_user.admin
        }

        mock_get_user.return_value = mock_user

        response = client.post('/users/login', json=payload)

    assert response.status_code == 200, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert data['user']['email'] == sample_user.email


def test_get_user(client, sample_user, app):
    """Test fetching a user by ID."""
    with app.app_context():
        response = client.get(f'/users/{sample_user.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == sample_user.id
        assert data['name'] == sample_user.name
        assert data['email'] == sample_user.email
        assert data['profile_pic_url'] == sample_user.profile_pic_url
