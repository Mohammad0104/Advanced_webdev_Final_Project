from flask import Flask
from extensions import db  # Import the single SQLAlchemy instance
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

    db.init_app(app)  # Initialize the db instance with the app
    Migrate(app, db)
    CORS(app, supports_credentials=True)

    with app.app_context():
        from models.user import User  # Import models here
        db.create_all()

    # Register Blueprints
    app.register_blueprint(oauth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(review_blueprint)

    return app
