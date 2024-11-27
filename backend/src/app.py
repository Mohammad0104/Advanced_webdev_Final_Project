from flask import Flask
from models import db
from config.config import Config
import os
from controllers.oauth_controller import oauth_bp
from controllers.product_controller import product_bp
from controllers.user_controller import user_blueprint
from controllers.review_controller import review_blueprint
from controllers.order_controller import order_bp
from controllers.cart_controller import cart_bp
from controllers.cart_item_controller import cart_item_bp
from controllers.payment_controller import payment_bp
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(config=None):
    app = Flask(__name__)
    
    # Load the configuration from the Config object or the passed config
    app.config.from_object(Config)
    
    if config:
        app.config.update(config)

    # Enable CORS for all routes (you can specify origins if needed)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # Alternatively, for restricted CORS access:
    # CORS(app, supports_credentials=True, origins=['http://localhost:3000'], debug=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Set secret key for sessions
    app.secret_key = Config.SECRET_KEY
    
    # Register blueprints (modular routes)
    app.register_blueprint(oauth_bp, url_prefix='/oauth')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(review_blueprint, url_prefix='/reviews')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(cart_item_bp, url_prefix='/cart_items')
    app.register_blueprint(payment_bp, url_prefix='/payments')

    # Create all tables if not in testing mode
    with app.app_context():
        if not app.config.get('TESTING', False):
            db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()

    # Set environment variables for OAuth configuration
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'  # Fixes issues where scope changes
    
    # Run the Flask app on localhost:8080 in debug mode
    app.run(host='localhost', port=8080, debug=True)