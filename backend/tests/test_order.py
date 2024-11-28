import pytest
from flask import Flask
from models import db
from models.user import User
from models.order import Order
from models.cart import Cart
from models.order_item import OrderItem
from models.cart_item import CartItem
from models.product import Product
from datetime import datetime
from services.order_service import create_order, get_all_orders_by_userid
from controllers.order_controller import order_bp


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
        app.register_blueprint(order_bp, url_prefix="/api")
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
        db.session.query(OrderItem).delete()
        db.session.query(Cart).delete()
        db.session.query(Order).delete()
        db.session.query(Product).delete()
        db.session.query(User).delete()

        # Create users
        user1 = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            profile_pic_url="http://example.com/profile1.jpg",
            admin=False
        )
        user2 = User(
            id=2,
            name="Jane Doe",
            email="jane@example.com",
            profile_pic_url="http://example.com/profile2.jpg",
            admin=False
        )
        db.session.add_all([user1, user2])

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
            featured=False,
            youth_size=False,
            brand="Brand A",
            sport="Sport A",
            date_listed=datetime.utcnow()
        )
        product2 = Product(
            id=2,
            name="Product 2",
            seller_id=2,
            price=75.0,
            gender="Unisex",
            size="L",
            condition="New",
            quantity=5,
            featured=False,
            youth_size=True,
            brand="Brand B",
            sport="Sport B",
            date_listed=datetime.utcnow()
        )
        db.session.add_all([product1, product2])

        # Create a cart for user1
        cart = Cart(
            id=1,
            user_id=1,
            subtotal=125.0
        )
        db.session.add(cart)

        # Add items to the cart
        cart_item1 = CartItem(
            cart_id=1,
            product_id=1,
            quantity=1
        )
        cart_item2 = CartItem(
            cart_id=1,
            product_id=2,
            quantity=1
        )
        db.session.add_all([cart_item1, cart_item2])

        # Create an order for user1
        order = Order(
            id=1,
            user_id=1,
            total=125.0,
            order_date=datetime.utcnow()
        )
        db.session.add(order)

        # Create order items
        order_item1 = OrderItem(
            order_id=1,
            product_name="Product 1",
            quantity=1,
            price=50.0
        )
        order_item2 = OrderItem(
            order_id=1,
            product_name="Product 2",
            quantity=1,
            price=75.0
        )
        db.session.add_all([order_item1, order_item2])
        db.session.commit()


def test_get_user_order_history(app, client, setup_database):
    """Test retrieving a user's order history."""
    response = client.get(f'/api/orders/user/1')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data['orders']) == 1  
    assert data['orders'][0]['total'] == 125.0
    assert len(data['orders'][0]['items']) == 2


def test_create_order(app, client, setup_database):
    """Test creating an order from a user's cart."""
    response = client.post(f'/api/orders/create/1')
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    data = response.get_json()

    # Verify the created order
    assert data['order']['user_id'] == 1, "Order user_id mismatch"
    assert data['order']['total'] == 125.0, "Order total mismatch"
    assert len(data['order']['items']) == 2, "Order items count mismatch"

    # Verify the cart is emptied
    with app.app_context():
        cart = Cart.query.filter_by(user_id=1).first()
        assert cart is None, "Cart should be deleted after order creation"


def test_create_order_no_cart(app, client):
    """Test creating an order for a user with no cart."""
    response = client.post(f'/api/orders/create/999')  
    assert response.status_code == 500
    data = response.get_json()
    assert "Cart not found" in data['error']


def test_get_user_order_history_no_orders(app, client):
    """Test retrieving an order history for a user with no orders."""
    response = client.get(f'/api/orders/user/2')  
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['orders']) == 0
