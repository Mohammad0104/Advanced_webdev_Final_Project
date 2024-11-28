import requests
import json

# Define the API endpoint
url = "http://127.0.0.1:5000/create-payment-intent"  # Update if your app is running on a different host or port

# Test payload to simulate items and customer data
payload = {
    "items": [
        {"id": "premium", "quantity": 1}
    ],
    "customer": "test_customer_id_123"
}

# Set request headers
headers = {
    "Content-Type": "application/json"
}

def test_create_payment_intent():
    """
    Test the create-payment-intent endpoint.
    Sends a POST request and prints the response.
    """
    try:
        # Send POST request
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        # Print status code and response data
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.json()}")
    
    except Exception as e:
        # Print any exceptions that occur during the request
        print(f"Error: {e}")

if __name__ == "__main__":
    test_create_payment_intent()
