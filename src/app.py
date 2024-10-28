from flask import Flask
from models import db
from config import Config
import os
from controllers.oauth_controller import oauth_bp
# from flask_talisman import Talisman

def create_app():
  app = Flask(__name__)
  
  # Talisman(app, force_https=True)
  
  # Initialize extensions
  # db.init_app(app)
  
  app.secret_key = Config.SECRET_KEY
  
  # Register blueprints
  app.register_blueprint(oauth_bp)
    
  return app

if __name__ == '__main__':
  app = create_app()
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' # fixes issue where scope changes (happens with the optional google drive permission)
  app.run('localhost', 8080, debug=True)
  # app.run(debug=True)
