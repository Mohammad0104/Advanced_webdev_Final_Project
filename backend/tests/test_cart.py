import pytest
from src.models import db
from src.models.cart_model import Cart


@pytest.fixture
def cart_data():
    """
    Sample cart data for testing.
    """
    return {
        "user_id": 1,
        "subtotal": 50.0,
        "icon_urls": "https://example.com/icon1.png,https://example.com/icon2.png"
    }


def test_create_cart(test_client, cart_data):
    """
    Test creating a new cart.
    """
    response = test_client.post('/cart', json=cart_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['user_id'] == cart_data['user_id']
    assert data['subtotal'] == cart_data['subtotal']
    assert data['icon_urls'] == cart_data['icon_urls']


def test_get_cart(test_client, cart_data):
    """
    Test retrieving a cart by user ID.
    """
    # Create a cart to retrieve
    test_client.post('/cart', json=cart_data)

    response = test_client.get(f'/cart/{cart_data["user_id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user_id'] == cart_data['user_id']
    assert data['subtotal'] == cart_data['subtotal']
    assert data['icon_urls'] == cart_data['icon_urls']


def test_get_cart_invalid_user(test_client):
    """
    Test retrieving a cart for a non-existent user ID.
    """
    response = test_client.get('/cart/9999')  # Non-existent user ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Cart not found"


def test_update_cart(test_client, cart_data):
    """
    Test updating a cart's subtotal and icon URLs.
    """
    # Create a cart to update
    create_response = test_client.post('/cart', json=cart_data)
    cart_id = create_response.get_json()['id']

    updated_data = {"subtotal": 100.0, "icon_urls": "https://example.com/new_icon.png"}
    response = test_client.put(f'/cart/{cart_id}', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['subtotal'] == updated_data['subtotal']
    assert data['icon_urls'] == updated_data['icon_urls']


def test_update_cart_invalid_id(test_client):
    """
    Test updating a cart with an invalid cart ID.
    """
    updated_data = {"subtotal": 100.0}
    response = test_client.put('/cart/9999', json=updated_data)  # Non-existent cart ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Cart not found"


def test_delete_cart(test_client, cart_data):
    """
    Test deleting a cart.
    """
    # Create a cart to delete
    create_response = test_client.post('/cart', json=cart_data)
    cart_id = create_response.get_json()['id']

    response = test_client.delete(f'/cart/{cart_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == "Cart deleted successfully"

    # Verify the cart is deleted
    response = test_client.get(f'/cart/{cart_data["user_id"]}')
    assert response.status_code == 404


def test_delete_cart_invalid_id(test_client):
    """
    Test deleting a cart with an invalid cart ID.
    """
    response = test_client.delete('/cart/9999')  # Non-existent cart ID
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Cart not found"
