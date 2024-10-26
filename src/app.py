from flask import Flask
from models import db
from config import Config
from controllers.oauth_controller import oauth_bp

def create_app():
  app = Flask(__name__)
  
  # Initialize extensions
  # db.init_app(app)
  
  app.secret_key = Config.SECRET_KEY
  
  # Register blueprints
  app.register_blueprint(oauth_bp)
    
  return app

if __name__ == '__main__':
  app = create_app()
  app.run(debug=True)
