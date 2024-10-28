from flask import Blueprint, redirect, request, session, jsonify
from services.oauth.oauth_service import OAuthService
import requests
import google.oauth2.credentials

oauth_bp = Blueprint('oauth_bp', __name__)
oauth_service = OAuthService()

@oauth_bp.route('/')
def index():
    # options table (will be changed later.  For now the focus is on "Test the authentication flow directly")
    return print_index_table()

@oauth_bp.route('/authorize')
def authorize():
    """Starts the OAuth 2.0 authorization flow 

    Returns:
        Redirect user to the authorization URL
    """
    authorization_url, state = oauth_service.get_authorization_url()
    session['state'] = state  # Store state for verification
    
    # print("Authorization URL:", authorization_url)
    # print("Scopes being used:", oauth_service.SCOPES)
    return redirect(authorization_url)

@oauth_bp.route('/oauth2callback')
def oauth2callback():
    """Handles OAuth 2.0 callnack from the authorization server

    Returns:
        Redirect to the user info page
    """
    state = session['state']  # retrieve the state to verify
    authorization_response = request.url # get full callback URL
    
    # print("\n\nHEYYYY")
    # print(authorization_response)
    # print("\n\n")

    # fetch credentials
    credentials = oauth_service.fetch_token(authorization_response)
    
    if not credentials:
        return "Error fetching credentials", 400
    
    # store the credentials in the session
    session['credentials'] = OAuthService.credentials_to_dict(credentials)

    # return redirect('/test')
    return redirect('/user_info')

# @oauth_bp.route('/test')
# def test_api_request():
#     if not oauth_service.has_drive_scope(credentials):
#         print("Google Drive scope not granted. Skipping Drive operations.")
#         return  # or handle as needed
    
#     if 'credentials' not in session:
#         return redirect('/authorize')

#     credentials = google.oauth2.credentials.Credentials(
#         **session['credentials']
#     )

#     drive_service = oauth_service.get_drive_service(credentials)
#     files = drive_service.files().list().execute()

#     session['credentials'] = OAuthService.credentials_to_dict(credentials)  # Refresh credentials if necessary

#     return jsonify(**files)

@oauth_bp.route('/user_info')
def user_info():
    """Get and display user information.  To be used after authentication

    Returns:
        JSON or Redirect: JSON response with user info or redirection to the authorization route if credentials are missing
    """
    
    # if credentials are not stored in the session, redirect to the authorization route
    if 'credentials' not in session:
        return redirect('/authorize')

    # create credentials object from the session
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    # get user info with the access token
    user_info = oauth_service.get_user_info(credentials.token)
    
    # refresh credentials
    session['credentials'] = OAuthService.credentials_to_dict(credentials)

    # return user info as JSON
    return jsonify(user_info)

@oauth_bp.route('/revoke')
def revoke():
    """Revoke OAuth 2.0 credentials and log out the user

    Returns:
        Message indicating success or failure
    """
    
    # if credentials are not stored in the session redirect to the authorization route
    if 'credentials' not in session:
        return redirect('/authorize')

    # create credentials object from the session
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    # make POST request to revoke the access token
    revoke = requests.post(
        'https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token}, # send token to be revoked
        headers={'content-type': 'application/x-www-form-urlencoded'}
    )

    if revoke.status_code == 200:
        return 'Credentials successfully revoked.<br><br>' + print_index_table()  # if successful
    else:
        return 'An error occurred.<br><br>' + print_index_table() # if failed

@oauth_bp.route('/clear')
def clear_credentials():
    """Clear the credentials from the session

    Returns:
        Message confirming that the credentials were removed from the session
    """
    
    # clear all session data
    session.clear()
    
    # return confirmation message
    return 'Credentials have been cleared.<br><br>' + print_index_table()


# to be changed later (from default google example)
def print_index_table():
    return ('<table>'
            '<tr><td><a href="/test">Test an API request</a></td>'
            '<td>Submit an API request and see a formatted JSON response.</td></tr>'
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>'
            '<td>Go directly to the authorization flow.</td></tr>'
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>'
            '<td>Revoke the access token associated with the current user session.</td></tr>'
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>'
            '<td>Clear the access token currently stored in the user session.</td></tr>'
            '</table>')
