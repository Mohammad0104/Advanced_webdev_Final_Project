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
        # # Setup env vars beforehand 
        # stripe_keys = {
        #     "secret_key": os.environ["STRIPE_SECRET_KEY"],
        #     "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
        # }

        # stripe.api_key = stripe_keys["secret_key"]
        # data = json.loads(request.data)
        # print(data)
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,  # Adjust according to the price of "Premium"
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )
        
        # intent = stripe.PaymentIntent.create(
        #     amount=2000,
        #     currency='eur',
        #     automatic_payment_methods={
        #         'enabled': True,
        #     },
        #     # Again, I am providing a user_uuid, so I can identify who is making the payment later
        #     metadata={
        #         'customer': data['customer']
        #     },
        # )
        
        # client_secret = intent['client_secret']
        # print(f"Stripe clientSecret: {client_secret}")  # Ensure it's properly set

        # return jsonify ({
        #     'clientSecret': intent['client_secret']
        # })
          # Log the client secret to verify it
        print(f"Stripe clientSecret: {payment_intent.client_secret}")

        # Send the client secret to the frontend
        return jsonify({'clientSecret': payment_intent.client_secret})

    except Exception as e:
        return jsonify(error=str(e)), 403