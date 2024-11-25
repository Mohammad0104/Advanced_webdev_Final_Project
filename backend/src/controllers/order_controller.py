from flask import Blueprint, request, jsonify
from datetime import datetime
from services import order_service

from services.auth import login_required

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_order_history(user_id):
    try:
        # Fetch the orders for the user from the order service
        orders = order_service.get_orders_by_user_id(user_id).all()
        
        # Return the orders in JSON format
        return jsonify({"orders": orders}), 200
    except Exception as e:
        # Handle exceptions (e.g., database errors, user not found, etc.)
        return jsonify({"error": str(e)}), 500