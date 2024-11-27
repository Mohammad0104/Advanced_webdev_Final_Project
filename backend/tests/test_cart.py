import pytest
from flask import Flask
from models import db
from models.cart import Cart
from models.user import User
from models.product import Product
from controllers.cart_controller import cart_bp
from datetime import datetime

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

        # Create products with required fields, including 'brand'
        product1 = Product(
            id=1,
            name="Product 1",
            seller_id=1,
            price=50.0,
            gender="Unisex",
            size="M",
            condition="New",
            youth_size=False,
            brand="Brand A",  # Provide a value for the NOT NULL field 'brand'
            sport="Running",  # Adding any missing required field
            date_listed=datetime.utcnow(),
            year_product_made=2022,
            avg_rating=0.0
        )
        product2 = Product(
            id=2,
            name="Product 2",
            seller_id=2,
            price=50.0,
            gender="Unisex",
            size="L",
            condition="Used",
            youth_size=True,
            brand="Brand B",  # Provide a value for the NOT NULL field 'brand'
            sport="Football",  # Adding any missing required field
            date_listed=datetime.utcnow(),
            year_product_made=2021,
            avg_rating=0.0
        )
        db.session.add_all([product1, product2])

        # Create a cart for user1
        cart = Cart(id=1, user_id=1, subtotal=100.0)
        db.session.add(cart)

        db.session.commit()




def test_get_cart(client, setup_database):
    """Test retrieving a cart by user ID."""
    response = client.get('/api/cart/1')
    assert response.status_code == 200

    data = response.get_json()
    assert data['user_id'] == 1
    assert data['subtotal'] == 100.0


def test_get_cart_not_found(client):
    """Test retrieving a cart for a non-existent user."""
    response = client.get('/api/cart/999')  # Non-existent user
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


def test_update_cart(client, setup_database):
    """Test updating a cart's subtotal."""

    # Ensure that cart 1 exists and has items
    cart_response = client.get('/api/cart/1')
    assert cart_response.status_code == 200  # Ensure the cart exists
    
    cart_data = cart_response.get_json()

    # If cart has no items, the cart is not functioning as expected
    assert len(cart_data['items']) > 0, "Cart should have at least one item"

    # Update the cart subtotal
    response = client.put('/api/cart/1', json={"subtotal": 200.0})
    
    # Assert that the response status is 200
    assert response.status_code == 200  # Expect 200 OK

    # Get the updated cart details
    data = response.get_json()

    # Assert the subtotal is updated correctly
    assert data['subtotal'] == 200.0, f"Expected subtotal to be 200.0, but got {data['subtotal']}"

    # Ensure the cart has the correct number of items and each item matches the expected
    assert len(data['items']) == len(cart_data['items'])  # Ensure the number of items is the same
    for item in data['items']:
        assert 'product_id' in item
        assert 'quantity' in item
        assert 'product_name' in item
        assert 'product_price' in item





def test_update_cart_not_found(client):
    """Test updating a cart that does not exist."""
    response = client.put('/api/cart/999', json={"subtotal": 200.0, "product_id": 1, "quantity": 2})
    assert response.status_code == 404
    data = response.get_json()
    assert "Cart not found" in data['error']


def test_delete_cart(client, setup_database):
    """Test deleting a cart."""
    response = client.delete('/api/cart/1')
    assert response.status_code == 200

    data = response.get_json()
    assert "Cart deleted successfully" in data['message']


def test_delete_cart_not_found(client):
    """Test deleting a cart that does not exist."""
    response = client.delete('/api/cart/999')
    assert response.status_code == 404
    data = response.get_json()
    assert "Cart not found" in data['error']
