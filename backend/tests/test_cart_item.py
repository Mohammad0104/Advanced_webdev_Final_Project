import pytest
from app import create_app, db
from models.user import User
from models.product import Product
from models.cart import Cart
import datetime

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
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
        db.session.add(user1)

        # Create products
        product1 = Product(
            id=1,
            name="Product 1",
            seller_id=1,
            price=50.0,
            gender="Unisex",
            size="M",
            condition="New",
            brand="Brand A",
            youth_size=False,
            sport="Soccer",
            date_listed=datetime.datetime.now(),
        )
        product2 = Product(
            id=2,
            name="Product 2",
            seller_id=1,
            price=30.0,
            gender="Unisex",
            size="L",
            condition="Used",
            brand="Brand B",
            youth_size=True,
            sport="Basketball",
            date_listed=datetime.datetime.now(),
        )
        db.session.add_all([product1, product2])

        # Create a cart for user1
        cart = Cart(id=1, user_id=1, subtotal=0.0)
        db.session.add(cart)

        db.session.commit()

def test_add_to_cart(client, setup_database):
    """Test adding a product to the cart."""
    response = client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})  # Ensure the path is correct
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["subtotal"] == 100.0
    assert len(data["items"]) == 1

def test_add_to_cart_existing_product(client, setup_database):
    """Test adding more of an existing product to the cart."""
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})  # Add product first time
    response = client.post("/cart/1/add", json={"product_id": 1, "quantity": 3})  # Add more of the same product
    assert response.status_code == 201
    data = response.get_json()
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 5
    assert data["subtotal"] == 250.0

def test_remove_from_cart(client, setup_database):
    """Test removing an item from the cart."""
    client.post("/cart/1/add", json={"product_id": 1, "quantity": 2})  # Add product first
    response = client.delete("/cart/1/remove", json={"cart_item_id": 1})  # Ensure the path is correct
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["items"]) == 0
    assert data["subtotal"] == 0.0

def test_remove_nonexistent_item(client, setup_database):
    """Test removing a nonexistent item from the cart."""
    response = client.delete("/cart/1/remove", json={"cart_item_id": 999})  # Nonexistent cart item ID
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None  # Ensure a response is returned
    assert "error" in data  # Ensure the error message is present
    assert data["error"] == "Item not found"  # Match the exact error message from the backend
