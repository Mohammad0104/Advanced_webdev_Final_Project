import json
from models.user import User

def test_get_user_by_id(test_client, add_user):
    """Test fetching a user by ID."""
    # Arrange: Add a sample user
    user = add_user(name="John Doe", email="john.doe@example.com", profile_pic_url="https://example.com/john.png")
    
    # Act: Make a GET request to fetch the user by ID
    response = test_client.get(f'/users/{user.id}')
    
    # Assert: Check if the response is correct
    assert response.status_code == 200
    assert response.json['id'] == user.id
    assert response.json['name'] == "John Doe"


def test_get_user_by_invalid_id(test_client):
    """Test fetching a user with an invalid ID."""
    # Act: Make a GET request with a non-existent user ID
    response = test_client.get('/users/999')
    
    # Assert: Check if the response is a 404
    assert response.status_code == 404
    assert response.json['message'] == "User not found"


def test_create_user(test_client):
    """Test creating a new user."""
    # Arrange: Prepare user data
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "profile_pic_url": "https://example.com/jane.png",
        "password": "securepassword123"
    }
    
    # Act: Make a POST request to register the user
    response = test_client.post('/users/register', data=json.dumps(user_data), content_type='application/json')
    
    # Assert: Check if the user was created successfully
    assert response.status_code == 201
    assert response.json['name'] == "Jane Doe"
    assert response.json['email'] == "jane.doe@example.com"


def test_create_user_with_existing_email(test_client, add_user):
    """Test trying to create a user with an existing email."""
    # Arrange: Add a user with the same email
    add_user(name="Existing User", email="duplicate@example.com", profile_pic_url="https://example.com/existing.png")
    user_data = {
        "name": "Jane Doe",
        "email": "duplicate@example.com",
        "profile_pic_url": "https://example.com/jane.png",
        "password": "securepassword123"
    }
    
    # Act: Make a POST request to register the user
    response = test_client.post('/users/register', data=json.dumps(user_data), content_type='application/json')
    
    # Assert: Check if the response indicates a conflict
    assert response.status_code == 409
    assert response.json['message'] == "Email already exists"


def test_login_user(test_client, add_user):
    """Test logging in an existing user."""
    # Arrange: Add a user
    add_user(
        name="John Login",
        email="login@example.com",
        profile_pic_url="https://example.com/login.png",
        admin=False
    )
    login_data = {"email": "login@example.com", "password": "securepassword123"}
    
    # Act: Make a POST request to login
    response = test_client.post('/users/login', data=json.dumps(login_data), content_type='application/json')
    
    # Assert: Check if the login was successful
    assert response.status_code == 200
    assert response.json['message'] == "Login successful"


def test_update_user_name(test_client, add_user):
    """Test updating the name of an existing user."""
    # Arrange: Add a sample user
    user = add_user(name="Old Name", email="update@example.com", profile_pic_url="https://example.com/old.png")
    update_data = {"new_name": "New Name"}
    
    # Act: Make a PUT request to update the user's name
    response = test_client.put(f'/users/{user.id}', data=json.dumps(update_data), content_type='application/json')
    
    # Assert: Check if the name was updated successfully
    assert response.status_code == 200
    assert response.json['message'] == "User's name updated successfully to: New Name"


def test_update_user_name_invalid_id(test_client):
    """Test updating a user's name with an invalid ID."""
    # Act: Make a PUT request for a non-existent user
    update_data = {"new_name": "New Name"}
    response = test_client.put('/users/999', data=json.dumps(update_data), content_type='application/json')
    
    # Assert: Check if the response indicates a failure
    assert response.status_code == 404
    assert response.json['error'] == "User with the specified ID not found."


def test_get_user_by_email(test_client, add_user):
    """Test fetching a user by email."""
    # Arrange: Add a user
    user = add_user(name="Jane Doe", email="jane@example.com", profile_pic_url="https://example.com/jane.png")
    
    # Act: Make a GET request to fetch the user by email
    response = test_client.get(f'/users/email/{user.email}')
    
    # Assert: Check if the response is correct
    assert response.status_code == 200
    assert response.json['email'] == "jane@example.com"
