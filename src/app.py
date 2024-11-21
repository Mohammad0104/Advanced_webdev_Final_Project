from flask import Flask
from models import db
from config.config import Config
import os
from controllers.oauth_controller import oauth_bp
from controllers.product_controller import product_bp
from flask_migrate import Migrate
from flask_cors import CORS

# from flask_talisman import Talisman

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  
  CORS(app, origins=["http://localhost:3000"])  # Allow requests from the frontend
  
  # Talisman(app, force_https=True)
  
  # Initialize extensions
  db.init_app(app)
  migrate = Migrate(app, db)
  
  app.secret_key = Config.SECRET_KEY
  
  # Register blueprints
  app.register_blueprint(oauth_bp)
  app.register_blueprint(product_bp)
  
  with app.app_context():
    if not app.config.get('TESTING', False):
      db.create_all()
    
  return app

if __name__ == '__main__':
  app = create_app()
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' # fixes issue where scope changes (happens with the optional google drive permission)
  app.run('localhost', 8080, debug=True)
  # app.run(debug=True)