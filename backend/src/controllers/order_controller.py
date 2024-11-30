from flask import Blueprint, request, jsonify
from datetime import datetime
from services import order_service
from services.auth import login_required

# blueprint
order_bp = Blueprint('order_bp', __name__)


@order_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_order_history(user_id: int):
    """Endpoint to get the order history for a user

    Args:
        user_id (int): the id of the user to get the orders for

    Returns:
        JSON: JSON message with a list of the orders or an error message
    """
    try:
        # Fetch the orders for the user from the order service
        orders = order_service.get_all_orders_by_userid(user_id)
        
        orders_dict = [order.to_dict() for order in orders]
        
        # Return the orders in JSON format
        return jsonify({"orders": orders_dict}), 200
    except Exception as e:
        # Handle exceptions (e.g., database errors, user not found, etc.)
        return jsonify({"error": str(e)}), 500


@order_bp.route('/orders/create/<int:user_id>', methods=['POST'])
def create_order(user_id: int):
    """Endpoint to create a new order for the user

    Args:
        user_id (int): the id of the user who is making an order

    Returns:
        JSON: JSON message with the new order or error message
    """
    try:
        # Create an order for the given user
        new_order = order_service.create_order(user_id)
        return jsonify({"order": new_order.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500