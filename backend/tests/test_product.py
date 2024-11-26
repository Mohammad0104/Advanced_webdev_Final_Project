import pytest
import base64
from datetime import datetime
from src.models import db
from src.models.product import Product


@pytest.fixture
def product_data():
    """
    Sample product data for testing.
    """
    return {
        "seller_id": 1,
        "name": "Test Product",
        "description": "A great product for testing.",
        "price": 29.99,
        "gender": "Unisex",
        "size": "M",
        "youth_size": False,
        "featured": True,
        "brand": "TestBrand",
        "sport": "Basketball",
        "quantity": 10,
        "condition": "New",
        "image": "data:image/png;base64," + base64.b64encode(b"test_image_data").decode("utf-8"),
        "year_product_made": "2023",
        "avg_rating": 4.5
    }


def test_create_new_product(test_client, product_data):
    """
    Test creating a new product.
    """
    response = test_client.post('/create_product', json=product_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == "Product created successfully"
    assert data['product']['name'] == product_data['name']


def test_get_all_products(test_client, product_data):
    """
    Test fetching all products.
    """
    # Create a product to ensure the database is not empty
    test_client.post('/create_product', json=product_data)

    response = test_client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert 'products' in data
    assert len(data['products']) > 0
    assert any(product['name'] == product_data['name'] for product in data['products'])


def test_get_product_by_id(test_client, product_data):
    """
    Test fetching a product by ID.
    """
    # Create a product to fetch
    create_response = test_client.post('/create_product', json=product_data)
    product_id = create_response.get_json()['product']['id']

    response = test_client.get(f'/product/{product_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['product']['id'] == product_id
    assert data['product']['name'] == product_data['name']


def test_get_product_by_invalid_id(test_client):
    """
    Test fetching a product with an invalid ID.
    """
    response = test_client.get('/product/999999')  # Non-existing ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Product not found"


def test_update_product(test_client, product_data):
    """
    Test updating an existing product.
    """
    # Create a product to update
    create_response = test_client.post('/create_product', json=product_data)
    product_id = create_response.get_json()['product']['id']

    updated_data = {"name": "Updated Product Name", "price": 19.99}
    response = test_client.put(f'/product/{product_id}', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Product updated successfully"
    assert data['product']['name'] == updated_data['name']
    assert data['product']['price'] == updated_data['price']


def test_update_product_invalid_id(test_client):
    """
    Test updating a product with an invalid ID.
    """
    updated_data = {"name": "Updated Name"}
    response = test_client.put('/product/999999', json=updated_data)  # Non-existing ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Product not found"


def test_delete_product(test_client, product_data):
    """
    Test deleting a product.
    """
    # Create a product to delete
    create_response = test_client.post('/create_product', json=product_data)
    product_id = create_response.get_json()['product']['id']

    response = test_client.delete(f'/product/{product_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == "Product deleted successfully"

    # Verify the product is deleted
    response = test_client.get(f'/product/{product_id}')
    assert response.status_code == 404


def test_delete_product_invalid_id(test_client):
    """
    Test deleting a product with an invalid ID.
    """
    response = test_client.delete('/product/999999')  # Non-existing ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Product not found"
