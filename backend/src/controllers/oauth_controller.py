from flask import Blueprint, redirect, request, session, jsonify, url_for
from flask_cors import cross_origin
from services.auth import login_required
from services.oauth.oauth_service import OAuthService
import requests
import google.oauth2.credentials


# user service
from services import user_service


# oauth service
oauth_bp = Blueprint('oauth_bp', __name__)
oauth_service = OAuthService()


@oauth_bp.route('/authorize')
@cross_origin()
def authorize():
    """Starts the OAuth 2.0 authorization flow (the login page)

    Returns:
        Redirect user to the authorization URL
    """
    session['original_url'] = request.args.get('next', 'http://localhost:3000/profile')  # Store the 'next' URL or the current URL
    authorization_url, state = oauth_service.get_authorization_url()
    session['state'] = state  # Store state for verification
    
    return redirect(authorization_url)


@oauth_bp.route('/oauth2callback')
@cross_origin()
def oauth2callback():
    """Handles OAuth 2.0 callnack from the authorization server

    Returns:
        Redirect to the original url that the user was on before the redirect to login
    """
    state = session['state']  # retrieve the state to verify
    authorization_response = request.url # get full callback URL

    # fetch credentials
    credentials = oauth_service.fetch_token(authorization_response)
    
    print(OAuthService.credentials_to_dict(credentials))
    
    if not credentials:
        return "Error fetching credentials", 400
    
    # store the credentials in the session
    session['credentials'] = OAuthService.credentials_to_dict(credentials)
    
    # get user info
    user_info = oauth_service.get_user_info(credentials.token)
    
    print('\n\n\n')
    print(user_info)

    # add user to db if not already in
    if user_info:
        user = user_service.get_user_by_email(user_info.get('email'))
        
        if not user:
            user = user_service.create_user(
                name = user_info.get('name'),
                email = user_info.get('email'),
                profile_pic_url = user_info.get('picture')
            )
        
        if not user:
            return "Error creating user", 400  # Handle the case where the user couldn't be created
        
        # add the id to the session (will be used for @login_required)
        session['user_id'] = user.id

    # Retrieve the original URL the user was trying to access
    original_url = session.get('original_url', '/profile')  # Default to '/profile' if not set

    # Clear session data to prevent reuse
    session.pop('original_url', None)

    # redirect back to previous screen
    return redirect(original_url)


@oauth_bp.route('/user_info')
@cross_origin()
@login_required
def user_info():
    """Get and display user information.  To be used after authentication

    Returns:
        JSON or Redirect: JSON response with user info or redirection to the authorization route if credentials are missing
    """
    try:
        # create credentials object from the session
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])

        # get user info with the access token
        user_info = oauth_service.get_user_info(credentials.token)
    
        # refresh credentials
        session['credentials'] = OAuthService.credentials_to_dict(credentials)
    except Exception as e:
        print('Error:', str(e))
        return

    # return user info as JSON
    return jsonify(user_info)


@oauth_bp.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    """Endpoint used to logout user

    Returns:
        redirect or JSON: Redirect back to the home page or JSON message if there's an error
    """
    try:
        # if there are credentials in the session
        if 'credentials' in session:
            try:
                # Revoke the token or perform any other necessary actions
                oauth_service.revoke_token(session['credentials']['token'])
            except Exception as e:
                print(f"Error during token revocation: {e}")
        
        # redirect back to the home page
        return redirect('http://localhost:3000/')
    except Exception as e:
        print(f"Error logging out: {e}")
        return jsonify({"error": "Logout failed"}), 500


@oauth_bp.route('/revoke')
@cross_origin()
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
        return 'Credentials successfully revoked.'
    else:
        return 'An error occurred.<br><br>'


@oauth_bp.route('/check_login_status', methods=['GET'])
@cross_origin()
def check_login():
    """Endpoint used to check if there is a user logged in

    Returns:
        JSON: JSON message with a true for logged in or false
    """
    is_logged_in = 'credentials' in session
    return jsonify({'logged_in': is_logged_in})
