import os
from flask import jsonify
import google_auth_oauthlib.flow
import googleapiclient.discovery
import requests
from .config import Config

class OAuthService:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current file
    CLIENT_SECRETS_FILE = os.path.join(base_dir, 'client_secret.json')  # Full path to client_secret.json
    # CLIENT_SECRETS_FILE = "client_secret.json"
    # SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    
    # starting scopes (permissions)
    SCOPES = [
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'openid',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
    ]

    # for google drive things (not important now)
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v2'

    def __init__(self):
        """Initialize the Google OAuth 2.0 authentication flow object
        """
        self.flow = None

    def create_flow(self):
        """Creates the Google OAuth 2.0 authentication flow object using the
        information from the client secret file and scopes
        """
        self.flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE, scopes=self.SCOPES
        )
        
        # setting the URI where Google will send the user back to after
        # authorzing the app
        self.flow.redirect_uri = self.get_redirect_uri()

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
        """Generates authorization URL for OAuth 2.0.
        The URL is used to redirect the user to the Google authorization page, where they
        grant permission to access their account

        Returns:
            tuple: containing:
                - str: Authorization URL to redirect the user to
                - str: State parameter for maintaining state between request and callback
        """
        # create the authentication flow
        self.create_flow()
        
        # generate tuple
        authorization_url, state = self.flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state
    
    def fetch_token(self, authorization_response):
        """Fetches the credetials after authentication.
        Exchanges the authorization code in the authorization
        response for the access and refresh tokens.

        Args:
            authorization_response (str): Full URL or string response containing the authorization code

        Returns:
            google.oauth2.credentials.Credentials: Instance/object containing access and refresh tokens, 
            token expiration time, and granted scopes
        """
        
        self.flow.fetch_token(authorization_response=authorization_response)
        return self.flow.credentials

    def get_drive_service(self, credentials):
        if not self.has_drive_scope(credentials):
            print("Google Drive scope not granted. Skipping Drive operations.")
            return

        return googleapiclient.discovery.build(
            self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials
        )
        
    def get_user_info(self, access_token):
        """Get the user's information

        Args:
            access_token (str): OAuth 2.0 access token

        Returns:
            dict or None: Returns a dictionary with user info.  On failure it returns None
        """
        
        # authentication header
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # send HTTP GET request to the specificied URL, with the authentication header 
        response = requests.get(Config.USER_API_URL, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # if successful
        else:
            print("Failed to fetch user info:", response.status_code, response.text)
            return None

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
