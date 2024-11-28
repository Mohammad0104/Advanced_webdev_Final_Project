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
    data = request.json
    items = data.get('items', [])
    customer = data.get('customer', '')

    try:
        # Log the loaded Stripe key to confirm it's being loaded
        stripe_api_key = os.getenv("STRIPE_SECRET_KEY")
        if not stripe_api_key:
            return jsonify(error="Stripe API key not found"), 403
        
        print(f"Stripe API Key Loaded: {stripe_api_key}")  # For debugging purposes
        
        stripe.api_key = stripe_api_key
        
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )
        
        print(f"Stripe clientSecret: {payment_intent.client_secret}")

        # Send the client secret to the frontend
        return jsonify({'clientSecret': payment_intent.client_secret})

    except Exception as e:
        print(f"Error: {e}")  # Debugging exception
        return jsonify(error=str(e)), 403
