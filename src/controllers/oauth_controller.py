from flask import Blueprint, redirect, request, session, url_for, jsonify
from services.oauth.oauth_service import OAuthService

oauth_bp = Blueprint('oauth_bp', __name__)
google_oauth_service = OAuthService()

@oauth_bp.route('/')
def login():
  return redirect(google_oauth_service.get_auth_url())

@oauth_bp.route('/callback')
def callback():
  code = request.args.get('code')
  access_token = google_oauth_service.exchange_code_for_token(code)
  
  if access_token:
    session['oauth_token'] = access_token
    user_info = google_oauth_service.get_user_info(access_token)
    
    if user_info:
      return jsonify({
        "message": f"Hello, {user_info['name']}.  You have logged in successfully using Google OAuth."
      })
    return jsonify({
      "error": "Login failed.  Try again."
    })


@oauth_bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('login'))