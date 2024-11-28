import pytest
import os
import sys

<<<<<<< Updated upstream
# Add the src directory to Python's module search dpath
=======

>>>>>>> Stashed changes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from models import db
from controllers.user_controller import user_blueprint
from models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
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

    # Cleanup the database after each test
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Add a sample user to the database."""
    user = User(
        name='Test User',
        email='test@example.com',
        password=generate_password_hash('password'),
        profile_pic_url='https://example.com/profile.jpg',
        admin=False,
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    return user
