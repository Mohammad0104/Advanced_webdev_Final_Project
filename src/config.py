import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  # JWT_SECRET_KEY = 'your_jwt_secret_key'
