import pytest
from flask import Flask
from datetime import datetime
from models import db
from models.product import Product
from models.user import User
from services.product_service import (
    get_product_by_id,
    get_all_products,
    create_product,
    update_product,
    delete_product,
)


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
        yield app


@pytest.fixture
def client(app):
    """Fixture to create a test client for the app."""
    return app.test_client()


@pytest.fixture
def setup_database(app):
    """Set up initial database content before each test."""
    with app.app_context():
        db.session.query(Product).delete()
        db.session.query(User).delete()

        # Add mock data
        user1 = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            profile_pic_url="http://example.com/profile1.jpg",
            admin=False,
        )
        user2 = User(
            id=2,
            name="Jane Doe",
            email="jane@example.com",
            profile_pic_url="http://example.com/profile2.jpg",
            admin=False,
        )

        product1 = Product(
            id=1,
            seller_id=1,
            name="Sample Product 1",
            description="A great product.",
            price=100.0,
            gender="Unisex",
            size="M",
            youth_size=False,
            featured=True,
            brand="Nike",
            sport="Running",
            quantity=10,
            condition="New",
            image=None,
            date_listed=datetime.utcnow(),
            year_product_made="2022",
            avg_rating=4.5,
        )
        product2 = Product(
            id=2,
            seller_id=2,
            name="Sample Product 2",
            description="Another great product.",
            price=200.0,
            gender="Male",
            size="L",
            youth_size=True,
            featured=False,
            brand="Adidas",
            sport="Football",
            quantity=5,
            condition="Used",
            image=None,
            date_listed=datetime.utcnow(),
            year_product_made="2021",
            avg_rating=4.0,
        )

        db.session.add_all([user1, user2, product1, product2])
        db.session.commit()


def test_get_product_by_id(app, client, setup_database):
    """Test retrieving a product by its ID."""
    with app.app_context():
        product = get_product_by_id(1)
        assert product is not None
        assert product.name == "Sample Product 1"

        product_not_found = get_product_by_id(999)
        assert product_not_found is None


def test_get_all_products(app, client, setup_database):
    """Test retrieving all products."""
    with app.app_context():
        products = get_all_products()
        assert len(products) == 2


def test_create_product(app, client, setup_database):
    """Test creating a new product."""
    with app.app_context():
        new_product = create_product(
            seller_id=1,
            name="New Product",
            description="A newly created product.",
            price=150.0,
            gender="Female",
            size="S",
            youth_size=False,
            featured=True,
            brand="Puma",
            sport="Yoga",
            quantity=15,
            condition="New",
            image=None,
            date_listed=datetime.utcnow(),
            year_product_made="2023",
            avg_rating=0.0,
        )

        assert new_product is not None
        assert new_product.name == "New Product"
        assert new_product.price == 150.0


def test_update_product(app, client, setup_database):
    """Test updating an existing product."""
    with app.app_context():
        updated_product = update_product(
            product_id=1,
            name="Updated Product Name",
            price=120.0,
            quantity=20,
        )

        assert updated_product is not None
        assert updated_product.name == "Updated Product Name"
        assert updated_product.price == 120.0
        assert updated_product.quantity == 20

        non_existent_update = update_product(product_id=999, name="Non-existent Product")
        assert non_existent_update is None


def test_delete_product(app, client, setup_database):
    """Test deleting a product."""
    with app.app_context():
        delete_message = delete_product(1)
        assert delete_message == "Product deleted successfully"

        product = get_product_by_id(1)
        assert product is None

        delete_non_existent = delete_product(999)
        assert delete_non_existent == "Product with this ID not found"
