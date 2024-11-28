import pytest
from flask import Flask
from datetime import datetime
from models import db
from models.user import User
from models.product import Product
from models.cart import Cart
from models.cart_item import CartItem 
from controllers.cart_controller import cart_bp


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
        app.register_blueprint(cart_bp, url_prefix="/api")
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
        # Create users
        user1 = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            profile_pic_url="http://example.com/johndoe.jpg",
            admin=False
        )
        user2 = User(
            id=2,
            name="Jane Doe",
            email="jane@example.com",
            profile_pic_url="http://example.com/janedoe.jpg",
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
            youth_size=False,
            brand="Brand A",
            sport="Running",
            date_listed=datetime.utcnow(),
            year_product_made=2022,
            avg_rating=0.0
        )
        product2 = Product(
            id=2,
            name="Product 2",
            seller_id=2,
            price=30.0,
            gender="Unisex",
            size="L",
            condition="Used",
            youth_size=True,
            brand="Brand B",
            sport="Football",
            date_listed=datetime.utcnow(),
            year_product_made=2021,
            avg_rating=0.0
        )
        db.session.add_all([product1, product2])

        # Create a cart for user1
        cart = Cart(id=1, user_id=1, subtotal=100.0)  
        db.session.add(cart)

        # Add items to the cart
        cart_item1 = CartItem(cart_id=1, product_id=1, quantity=1)
        cart_item2 = CartItem(cart_id=1, product_id=2, quantity=2)
        db.session.add_all([cart_item1, cart_item2])

        db.session.commit()


def test_get_cart(client, setup_database):
    """Test retrieving a cart by user ID."""
    response = client.get('/api/cart/1')
    assert response.status_code == 200

    data = response.get_json()
    assert data['user_id'] == 1
    assert data['subtotal'] == 100.0  
    assert len(data['items']) == 2
    assert data['items'][0]['product_id'] == 1
    assert data['items'][0]['quantity'] == 1
    assert data['items'][1]['product_id'] == 2
    assert data['items'][1]['quantity'] == 2


def test_get_cart_not_found(client):
    """Test retrieving a cart for a non-existent user."""
    response = client.get('/api/cart/999')  
    assert response.status_code == 404
    data = response.get_json()
    assert "Cart not found" in data['error']


def test_update_cart(client, setup_database):
    """Test updating a cart's subtotal and item quantities."""
    # Fetch cart details
    cart_response = client.get('/api/cart/1')
    assert cart_response.status_code == 200
    cart_data = cart_response.get_json()

    # Update the quantity of the first item
    product_id = cart_data['items'][0]['product_id']
    new_quantity = cart_data['items'][0]['quantity'] + 1

    response = client.put('/api/cart/1', json={
        "product_id": product_id,
        "quantity": new_quantity
    })
    assert response.status_code == 200

    updated_cart = response.get_json()
    updated_item = next(item for item in updated_cart['items'] if item['product_id'] == product_id)
    assert updated_item['quantity'] == new_quantity


def test_update_cart_not_found(client):
    """Test updating a cart that does not exist."""
    response = client.put('/api/cart/999', json={"product_id": 1, "quantity": 2})
    assert response.status_code == 404
    data = response.get_json()
    assert "Cart not found" in data['error']


def test_delete_cart(client, setup_database, app):
    """Test deleting a cart and associated items."""
    # Ensure the cart exists
    cart_response = client.get('/api/cart/1')
    assert cart_response.status_code == 200, "Cart not found before deletion"

    # Clean up cart items manually if cascading is not handled
    with app.app_context():
        cart_items = CartItem.query.filter_by(cart_id=1).all()
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()

    # Delete the cart
    response = client.delete('/api/cart/1')
    assert response.status_code == 200, "Failed to delete the cart"

    # Verify the cart is deleted
    cart_response = client.get('/api/cart/1')
    assert cart_response.status_code == 404, "Cart was not deleted"

    # Verify all associated cart items are deleted
    with app.app_context():
        remaining_items = CartItem.query.filter_by(cart_id=1).all()
        assert len(remaining_items) == 0, "Cart items were not deleted"



def test_delete_cart_not_found(client):
    """Test deleting a cart that does not exist."""
    response = client.delete('/api/cart/999')
    assert response.status_code == 404
    data = response.get_json()
    assert "Cart not found" in data['error']


def test_create_cart(client):
    """Test creating a new cart."""
    response = client.post('/api/cart', json={"user_id": 2, "subtotal": 50.0})
    assert response.status_code == 201

    data = response.get_json()
    assert data['user_id'] == 2
    assert data['subtotal'] == 50.0
