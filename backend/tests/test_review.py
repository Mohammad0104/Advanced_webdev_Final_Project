import pytest
from src.models import db
from src.models.review import Review
from src.models.user import User
from src.models.product import Product


@pytest.fixture
def review_data():
    """
    Sample review data for testing.
    """
    return {
        "reviewer_id": 1,
        "product_id": 1,
        "rating": 4.5,
        "explanation": "Great product!"
    }


@pytest.fixture
def setup_user_and_product(test_client):
    """
    Fixture to set up a user and product for review tests.
    """
    with test_client.application.app_context():
        # Create a user
        user = User(name="Test User", email="testuser@example.com", profile_pic_url="http://example.com/pic.png", admin=False)
        db.session.add(user)

        # Create a product
        product = Product(
            seller_id=1,
            name="Test Product",
            description="A test product",
            price=100.0,
            gender="Unisex",
            size="M",
            youth_size=False,
            featured=True,
            brand="Test Brand",
            sport="Test Sport",
            quantity=10,
            condition="New",
            date_listed="2024-01-01",
            year_product_made="2023",
            avg_rating=0.0
        )
        db.session.add(product)

        db.session.commit()


def test_create_review(test_client, setup_user_and_product, review_data):
    """
    Test creating a new review.
    """
    response = test_client.post('/create_review', json=review_data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert data['message'] == 'Review created successfully'


def test_create_review_missing_fields(test_client):
    """
    Test creating a review with missing required fields.
    """
    incomplete_data = {"reviewer_id": 1, "rating": 4.5}
    response = test_client.post('/create_review', json=incomplete_data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data
    assert 'Missing required fields' in data['message']


def test_retrieve_reviews(test_client, setup_user_and_product, review_data):
    """
    Test retrieving reviews for a specific product.
    """
    # Create a review
    test_client.post('/create_review', json=review_data)

    # Retrieve the reviews
    response = test_client.get(f'/reviews/product/{review_data["product_id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'reviews' in data
    assert len(data['reviews']) > 0
    assert data['reviews'][0]['product_id'] == review_data['product_id']


def test_retrieve_reviews_no_reviews(test_client, setup_user_and_product):
    """
    Test retrieving reviews for a product with no reviews.
    """
    response = test_client.get('/reviews/product/999')  # Non-existent product ID
    assert response.status_code == 200
    data = response.get_json()
    assert 'reviews' in data
    assert len(data['reviews']) == 0
    assert data['message'] == 'No reviews yet for this product'


def test_delete_review(test_client, setup_user_and_product, review_data):
    """
    Test deleting a review by ID.
    """
    # Create a review
    create_response = test_client.post('/create_review', json=review_data)
    review_id = create_response.get_json()['id']

    # Delete the review
    response = test_client.delete(f'/reviews/{review_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Review deleted successfully'

    # Verify the review is deleted
    response = test_client.get(f'/reviews/product/{review_data["product_id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['reviews']) == 0


def test_delete_review_invalid_id(test_client):
    """
    Test deleting a review with an invalid ID.
    """
    response = test_client.delete('/reviews/9999')  # Non-existent review ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Review not found'
