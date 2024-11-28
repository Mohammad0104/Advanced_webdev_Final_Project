import os
import json
from flask_cors import cross_origin
import stripe
from flask import jsonify, Blueprint, request
from dotenv import load_dotenv
load_dotenv()


payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/create-payment-intent', methods=['POST'])
@cross_origin()
def create_payment():
    """Create payment with external api (stripe)
    
    Initializes a PaymentIntent object with a fixed amount 
    and currency (although the amount does not matter). The client secret 
    returned by Stripe is sent back to the frontend for completing the 
    payment process

    Returns:
        JSON: A JSON response containing the client secret if successful, 
        or an error message with a 403 status code in case of failure
    """
    data = request.json
    items = data.get('items', [])
    customer = data.get('customer', '')

    try:
        # get stripe api key from .env file
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        # create PaymentIntent object
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )
        
        print(f"Stripe clientSecret: {payment_intent.client_secret}")

        # Send the client secret to the frontend
        return jsonify({'clientSecret': payment_intent.client_secret})

    except Exception as e:
        return jsonify(error=str(e)), 403