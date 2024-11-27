import pytest
from flask import Flask
from src.models import db
from src.models.review import Review
from src.models.user import User
from src.models.product import Product
from src.services.review_service import add_review, get_reviews_by_product, delete_review
from sqlalchemy.orm import configure_mappers
from datetime import datetime


@pytest.fixture
def app():
    """
    Fixture to create a Flask application for testing.
    """
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # Ensure all mappers are configured
        configure_mappers()
        db.create_all()  # Create database tables
        yield app


@pytest.fixture
def setup_database(app):
    """
    Fixture to populate the database with mock data for testing.
    """
    with app.app_context():
        # Create mock users
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

        # Create mock products
        product1 = Product(
            id=1,
            name="Sample Product 1",
            seller_id=1,
            price=100.00,
            gender="Unisex",
            size="M",
            condition="New",
            quantity=10,
            featured=True,
            youth_size=False,
            brand="Nike",
            sport="Running",
            date_listed=datetime.utcnow()
        )
        product2 = Product(
            id=2,
            name="Sample Product 2",
            seller_id=2,
            price=200.00,
            gender="Male",
            size="L",
            condition="Used",
            quantity=5,
            featured=False,
            youth_size=True,
            brand="Adidas",
            sport="Football",
            date_listed=datetime.utcnow()
        )

        db.session.add_all([user1, user2, product1, product2])
        db.session.commit()
        yield db


def test_add_review(app, setup_database):
    """
    Test adding a new review.
    """
    with app.app_context():
        reviewer_id = 1
        product_id = 1
        rating = 4.5
        explanation = "Great product!"

        # Call the function to add a review
        review = add_review(reviewer_id, product_id, rating, explanation)

        # Verify the review details
        assert review.reviewer_id == reviewer_id
        assert review.product_id == product_id
        assert review.rating == rating
        assert review.explanation == explanation
        assert isinstance(review.review_date, datetime)


def test_get_reviews_by_product(app, setup_database):
    """
    Test retrieving reviews for a specific product.
    """
    with app.app_context():
        # Add reviews to the database
        review1 = Review(reviewer_id=1, product_id=1, rating=4.0, explanation="Good product", review_date=datetime.utcnow())
        review2 = Review(reviewer_id=2, product_id=1, rating=5.0, explanation="Excellent!", review_date=datetime.utcnow())
        db.session.add_all([review1, review2])
        db.session.commit()

        # Call the function to get reviews
        reviews = get_reviews_by_product(1)

        # Verify the retrieved reviews
        assert len(reviews) == 2
        assert reviews[0]['rating'] == 4.0
        assert reviews[1]['rating'] == 5.0
        assert reviews[0]['product_id'] == 1


def test_delete_review(app, setup_database):
    """
    Test deleting an existing review.
    """
    with app.app_context():
        # Add a review to the database
        review = Review(reviewer_id=1, product_id=1, rating=4.0, explanation="Good product", review_date=datetime.utcnow())
        db.session.add(review)
        db.session.commit()

        # Call the function to delete the review
        result = delete_review(review.id)

        # Verify the review was deleted
        assert result is True
        assert Review.query.get(review.id) is None


def test_delete_nonexistent_review(app, setup_database):
    """
    Test deleting a non-existent review.
    """
    with app.app_context():
        # Attempt to delete a review that doesn't exist
        result = delete_review(999)

        # Verify the deletion was unsuccessful
        assert result is False
