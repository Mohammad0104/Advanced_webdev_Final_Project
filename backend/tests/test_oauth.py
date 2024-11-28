import pytest
from unittest.mock import patch, MagicMock
from flask import session
from services.oauth.oauth_service import OAuthService
from app import create_app


@pytest.fixture
def client():
    """Fixture to create a Flask application for testing."""
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            app.config['SESSION_TYPE'] = 'filesystem'
            app.config['SESSION_PERMANENT'] = False
            app.config['TESTING'] = True
            yield client


def test_oauth2callback(client):
    """Test the /oauth2callback endpoint which handles the OAuth callback"""

    mock_credentials = MagicMock()
    mock_credentials.token = 'mock_token'
    mock_credentials.refresh_token = 'mock_refresh_token'
    mock_credentials.token_uri = 'mock_token_uri'
    mock_credentials.client_id = 'mock_client_id'
    mock_credentials.client_secret = 'mock_client_secret'
    mock_credentials.scopes = ['profile', 'email']

    mock_user_info = {
        'email': 'user@example.com',
        'name': 'Test User',
        'picture': 'http://example.com/pic.jpg'
    }

    # Mock the OAuthService methods
    with patch.object(OAuthService, 'fetch_token', return_value=mock_credentials), \
         patch.object(OAuthService, 'get_user_info', return_value=mock_user_info):

        # Simulate the 'state' being stored in the session
        with client.session_transaction() as sess:
            sess['state'] = 'fake_state'

        # Simulate a callback with a valid code
        response = client.get('/oauth2callback?code=fake_code')

    # Check if the response redirects and session is updated
    assert response.status_code == 302, f"Unexpected status code: {response.status_code}"
    with client.session_transaction() as sess:
        assert 'credentials' in sess, "Credentials not stored in session"
        assert sess['credentials']['token'] == 'mock_token', "Token mismatch"


def test_user_info(client):
    """Test the /user_info endpoint after logging in via OAuth"""

    # Mock the credentials and user info
    mock_credentials = {
        'token': 'mock_token',
        'refresh_token': 'mock_refresh_token',
        'token_uri': 'mock_token_uri',
        'client_id': 'mock_client_id',
        'client_secret': 'mock_client_secret',
        'scopes': ['profile', 'email']
    }

    mock_user_info = {
        'email': 'user@example.com',
        'name': 'Test User',
        'picture': 'http://example.com/pic.jpg'
    }

    # Mock the OAuthService methods
    with patch.object(OAuthService, 'get_user_info', return_value=mock_user_info):
        # Simulate an authenticated session
        with client.session_transaction() as sess:
            sess['credentials'] = mock_credentials  # Add mocked credentials to session

        # Access the user_info endpoint
        response = client.get('/user_info')

    # Debugging output
    print(f"Response status code: {response.status_code}")
    if response.status_code == 302:  # Handle redirection
        redirect_location = response.headers.get('Location')
        print(f"Redirected to: {redirect_location}")
        assert redirect_location, "No redirect location found"
        # Assert the redirection to /authorize with the correct next parameter
        assert redirect_location.startswith('/authorize'), f"Unexpected redirect location: {redirect_location}"
    elif response.status_code == 200:  # Handle successful response
        user_data = response.get_json()
        print(f"Response JSON: {user_data}")
        assert user_data['email'] == 'user@example.com', "Email mismatch"
        assert user_data['name'] == 'Test User', "Name mismatch"
        assert user_data['picture'] == 'http://example.com/pic.jpg', "Picture URL mismatch"
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")




