import pytest
from flask import Flask
from models import db
from models.user import User
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from datetime import datetime
from controllers.cart_item_controller import cart_item_bp


@pytest.fixture
def app():
    """Fixture to create a Flask application for testing."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.register_blueprint(cart_item_bp, url_prefix="/api")
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Fixture to create a test client for the app."""
    return app.test_client()


@pytest.fixture
def setup_database(app):
    """Fixture to populate the database with mock data for testing."""
    with app.app_context():
        # Clear existing data
        db.session.query(CartItem).delete()
        db.session.query(Cart).delete()
        db.session.query(Product).delete()
        db.session.query(User).delete()

        # Create a user
        user = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            profile_pic_url="http://example.com/profile.jpg",
            admin=False
        )
        db.session.add(user)

        # Create products
        product1 = Product(
            id=1,
            name="Product 1",
            seller_id=1,
            price=50.0,
            gender="Unisex",
            size="M",
            condition="New",
            quantity=10,
            youth_size=False,  
            brand="Brand A",
            sport="Sport A",
            date_listed=datetime.utcnow()
        )
        product2 = Product(
            id=2,
            name="Product 2",
            seller_id=1,
            price=75.0,
            gender="Unisex",
            size="L",
            condition="New",
            quantity=5,
            youth_size=True,  
            brand="Brand B",
            sport="Sport B",
            date_listed=datetime.utcnow()
        )
        db.session.add_all([product1, product2])

        # Create a cart for the user
        cart = Cart(
            id=1,
            user_id=1,
            subtotal=0.0
        )
        db.session.add(cart)
        db.session.commit()


def test_add_to_cart(client, setup_database):
    """Test adding a product to the cart."""
    # Add a product to the cart
    response = client.post('/api/cart/1/add', json={'product_id': 1, 'quantity': 2})
    assert response.status_code == 201

    # Verify the cart's contents
    data = response.get_json()
    assert data['subtotal'] == 100.0  # 2 x 50.0
    assert len(data['items']) == 1
    assert data['items'][0]['product_id'] == 1
    assert data['items'][0]['quantity'] == 2


def test_remove_from_cart(client, setup_database):
    """Test removing a product from the cart."""
    # Add a product to the cart first
    client.post('/api/cart/1/add', json={'product_id': 1, 'quantity': 2})

    # Remove the product from the cart
    response = client.delete('/api/cart/1/remove', json={'cart_item_id': 1})
    assert response.status_code == 200

    # Verify the cart is now empty
    data = response.get_json()
    assert data['subtotal'] == 0.0
    assert len(data['items']) == 0




