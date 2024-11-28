import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from controllers.review_controller import review_blueprint


@pytest.fixture
def app():
    """Fixture to create a Flask application for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Register the review blueprint
    app.register_blueprint(review_blueprint)

    yield app


@pytest.fixture
def client(app):
    """Fixture to create a test client for the app."""
    return app.test_client()


def test_create_review(client):
    """Test creating a new review."""
    payload = {
        'reviewer_id': 1,
        'product_id': 101,
        'rating': 4.5,
        'explanation': 'Great product!',
    }

    # Patch the location where `add_review` is imported in `review_controller`
    with patch("controllers.review_controller.add_review") as mock_add_review:
        mock_review = MagicMock()
        mock_review.id = 123
        mock_add_review.return_value = mock_review

        response = client.post('/create_review', json=payload)

    # Validate the response
    assert response.status_code == 201, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['id'] == 123
    assert data['message'] == 'Review created successfully'


def test_retrieve_reviews(client):
    """Test retrieving reviews for a product."""
    product_id = 101

    # Patch the location where `get_reviews_by_product` is imported in `review_controller`
    with patch("controllers.review_controller.get_reviews_by_product") as mock_get_reviews:
        mock_get_reviews.return_value = [
            {
                'review_id': 1,
                'reviewer_id': 2,
                'rating': 4.5,
                'explanation': 'Great product!',
            },
            {
                'review_id': 2,
                'reviewer_id': 3,
                'rating': 3.0,
                'explanation': 'Good but could be better.',
            },
        ]

        response = client.get(f'/reviews/product/{product_id}')

    # Validate the response
    assert response.status_code == 200, f"Error: {response.get_json()}"
    data = response.get_json()
    assert len(data['reviews']) == 2
    assert data['reviews'][0]['review_id'] == 1
    assert data['reviews'][1]['rating'] == 3.0


def test_delete_review(client):
    """Test deleting a review."""
    review_id = 1

    # Patch the location where `delete_review` is imported in `review_controller`
    with patch("controllers.review_controller.delete_review") as mock_delete_review:
        mock_delete_review.return_value = True

        response = client.delete(f'/reviews/{review_id}')

    # Validate the response
    assert response.status_code == 200, f"Error: {response.get_json()}"
    data = response.get_json()
    assert data['message'] == 'Review deleted successfully'
