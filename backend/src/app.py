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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # CORS to accept requests from the frontend container
    CORS(app, resources={r"/*": {
        "origins": ["http://localhost:3000", "http://frontend:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})
    
    # initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # app secret key
    app.secret_key = Config.SECRET_KEY
    
    # register blueprints
    app.register_blueprint(oauth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(review_blueprint)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(cart_item_bp)
    app.register_blueprint(payment_bp)

    with app.app_context():
        if not app.config.get('TESTING', False):
            db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(host='0.0.0.0', port=8080, debug=True)
