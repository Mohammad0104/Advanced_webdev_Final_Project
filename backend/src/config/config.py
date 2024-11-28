import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'sqlite:///sports_marketplace.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  # SERVER_NAME = 'backend-container:8080'
  # JWT_SECRET_KEY = 'your_jwt_secret_key'
