import requests
from .config import Config

class OAuthService:

  def get_auth_url(self):
    return f"{Config.AUTHORIZATION_BASE_URL}?client_id={Config.CLIENT_ID}&redirect_uri={Config.REDIRECT_URI}&scope={Config.SCOPE}&response_type={Config.RESPONSE_TYPE}"

  def exchange_code_for_token(self, code):
    token_request_data = {
      'client_id': Config.CLIENT_ID,
      'client_secret': Config.CLIENT_SECRET,
      'code': code,
      'grant_type': 'authorization_code',
      'redirect_uri': Config.REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(Config.TOKEN_URL, data=token_request_data, headers=headers)
    token_response_data = response.json()
    return token_response_data.get('access_token')

  def get_user_info(self, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(Config.USER_API_URL, headers=headers)
    return user_info_response.json() if user_info_response.status_code == 200 else None
