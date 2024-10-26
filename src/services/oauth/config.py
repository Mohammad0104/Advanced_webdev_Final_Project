import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'google.env'))

class Config:
  CLIENT_ID = os.getenv('CLIENT_ID')
  CLIENT_SECRET = os.getenv('CLIENT_SECRET')
  AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
  TOKEN_URL = 'https://oauth2.googleapis.com/token'
  USER_API_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
  REDIRECT_URI = 'http://localhost:5000/callback'
  SCOPE = "openid%20email%20profile"
  RESPONSE_TYPE = "code"