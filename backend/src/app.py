from flask import Flask
from models import db
from config.config import Config
from flask_migrate import Migrate
from flask_cors import CORS

# Blueprints
from controllers.oauth_controller import oauth_bp
from controllers.product_controller import product_bp
from controllers.user_controller import user_blueprint
from controllers.review_controller import review_blueprint

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    CORS(app, supports_credentials=True)

    # Import models here to avoid circular imports
    with app.app_context():
        from models.user import User  # Import your models explicitly
        from models.product import Product  # Example model import
        db.create_all()

    # Register Blueprints
    app.register_blueprint(oauth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(review_blueprint)

    return app
