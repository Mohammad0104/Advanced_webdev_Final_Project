import os
from flask import jsonify, session
import google_auth_oauthlib.flow
import googleapiclient.discovery
import requests
from .config import Config


class OAuthService:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of the current file
    CLIENT_SECRETS_FILE = os.path.join(base_dir, 'client_secret.json')  # full path to client_secret.json
    
    # Updated scopes (removed unnecessary drive scope)
    SCOPES = [
        'openid', 
        'profile', 
        'email'
    ]

    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v2'


    def __init__(self):
        """Initialize the Google OAuth 2.0 authentication flow object"""
        self.flow = None


    def create_flow(self):
        """Creates the Google OAuth 2.0 authentication flow object using the
        information from the client secret file and scopes
        """
        try:
            self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                self.CLIENT_SECRETS_FILE, scopes=self.SCOPES
            )
            self.flow.redirect_uri = self.get_redirect_uri()
            print("OAuth flow created successfully.")
        except Exception as e:
            print("Error creating OAuth flow:", str(e))


    def get_redirect_uri(self):
        """To get the URI to be sent to after authorizing the app

        Returns:
            str: the URI
        """
        return 'http://localhost:8080/oauth2callback'
    
    
    def has_drive_scope(credentials):
        """To check if the drive scope is still included

        Args:
            credentials (google.oauth2.credentials.Credentials): Credentials object that has the user's access token and granted scopes

        Returns:
            bool: True if the Google Drive metadata scope ('https://www.googleapis.com/auth/drive.metadata.readonly') 
            is present. Otherwise, False is returned.
        """
        return 'https://www.googleapis.com/auth/drive.metadata.readonly' in credentials.scopes


    def get_authorization_url(self):
        """Generates authorization URL for OAuth 2.0."""
        try:
            self.create_flow()
            authorization_url, state = self.flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            print("Authorization URL generated:", authorization_url)
            return authorization_url, state
        except Exception as e:
            print("Error generating authorization URL:", str(e))
            return None, None
    
    
    def fetch_token(self, authorization_response):
        """Fetches the credentials after authentication."""
        try:
            print("Fetching token with response:", authorization_response)
            self.flow.fetch_token(authorization_response=authorization_response)
            print("Token fetched successfully.")
            return self.flow.credentials
        except Exception as e:
            print("Error fetching token:", str(e))
            return None
    
    
    def get_drive_service(self, credentials):
        if not self.has_drive_scope(credentials):
            print("Google Drive scope not granted. Skipping Drive operations.")
            return None

        return googleapiclient.discovery.build(
            self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials
        )
        
        
    def get_user_info(self, access_token):
        """Get the user's google account information

        Args:
            access_token (str): OAuth 2.0 access token

        Returns:
            dict or None: Returns a dictionary with user info. On failure it returns None
        """
        
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(Config.USER_API_URL, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # if successful
        else:
            print("Failed to fetch user info:", response.status_code, response.text)
            return None
    
    
    def revoke_token(self, token):
        """To revoke/remove credentials and user id from the session.
        Used when logging out

        Args:
            token (str): The google oauth token to be revoked
        """
        
        revoke_url = f'https://oauth2.googleapis.com/revoke?token={token}'
        
        try:
            # POST request to revoke the URL
            response = requests.post(revoke_url)
            
            session.pop('user_id', None)  # Remove user_id from session
            session.pop('credentials', None)  # Optionally, remove credentials if stored
            
            if response.status_code == 200:
                print("Token successfully revoked")
            else:
                print("Failed to revoke token")
        except Exception as e:
            print(f"Error revoking token: {e}")


    @staticmethod
    def credentials_to_dict(credentials):
        """Convert the credentials object into a dictionary

        Args:
            credentials (Credentials): OAuth 2.0 credentials object

        Returns:
            dict: Representation of the credentials in a dictionary
        """
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
