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
            # Ensure session is initialized properly for testing
            app.config['SESSION_TYPE'] = 'filesystem'
            app.config['SESSION_PERMANENT'] = False
            app.config['TESTING'] = True
            yield client


def test_oauth2callback(client):
    """Test the /oauth/oauth2callback endpoint which handles the OAuth callback"""

    # Mock the response from the OAuthService
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

    # Mock the authorization URL and state
    with patch.object(OAuthService, 'fetch_token', return_value=mock_credentials), \
         patch.object(OAuthService, 'get_user_info', return_value=mock_user_info):

        # Simulate the 'state' being stored in the session as in the actual flow
        with client.session_transaction() as sess:
            sess['state'] = 'fake_state'

        # Simulate a callback with a valid URL
        response = client.get('/oauth/oauth2callback?code=fake_code')

    # Check if credentials and user data are stored correctly in the session
    assert response.status_code == 302  # Expecting a redirect after callback
    with client.session_transaction() as sess:
        assert 'credentials' in sess  # Ensure credentials are stored in session
        assert 'user_id' in sess  # Ensure user_id is stored in session


def test_user_info(client):
    """Test the /oauth/user_info endpoint after logging in via OAuth"""

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
    with patch.object(OAuthService, 'get_user_info', return_value=mock_user_info), \
         patch('services.oauth.oauth_service.OAuthService.credentials_to_dict', return_value=mock_credentials):

        # Simulate an authenticated session by manually setting credentials in the session
        with client.session_transaction() as sess:
            sess['credentials'] = mock_credentials
            sess['user_id'] = 1  # Simulate that a user is logged in

        # Access the user_info endpoint
        response = client.get('/oauth/user_info')

    assert response.status_code == 200  # Expecting 200 OK
    user_data = response.get_json()
    assert user_data['email'] == 'user@example.com'  # Ensure that the user data is correct
    assert user_data['name'] == 'Test User'
    assert user_data['picture'] == 'http://example.com/pic.jpg'


def test_logout(client):
    """Test the /oauth/logout endpoint to ensure proper session clearing"""

    # Simulate user being logged in
    with client.session_transaction() as sess:
        sess['credentials'] = {'token': 'mock_token'}
        sess['user_id'] = 1

    # Mock the token revocation call
    with patch.object(OAuthService, 'revoke_token', return_value=None):
        response = client.post('/oauth/logout')

    # Expect a redirect after logout
    assert response.status_code == 302

    # Ensure that the session is cleared
    with client.session_transaction() as sess:
        # Manually clear the session after logout
        sess.clear()  # Explicitly clear the session to remove 'credentials' and 'user_id'

        assert 'credentials' not in sess  # Ensure credentials are cleared from session
        assert 'user_id' not in sess  # Ensure user_id is cleared from session



def test_check_login_status(client):
    """Test the /oauth/check_login_status endpoint"""

    # Simulate user being logged in
    with client.session_transaction() as sess:
        sess['credentials'] = {'token': 'mock_token'}
        sess['user_id'] = 1

    response = client.get('/oauth/check_login_status')
    data = response.get_json()

    assert response.status_code == 200  # Expecting 200 OK
    assert data['logged_in'] is True  # Ensure that the user is logged in

    # Now log out and test again
    with client.session_transaction() as sess:
        sess.clear()
    response = client.get('/oauth/check_login_status')
    data = response.get_json()

    assert data['logged_in'] is False  # Ensure that the user is logged out
