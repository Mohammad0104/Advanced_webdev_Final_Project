from flask import Blueprint, request, jsonify
from services.cart_service import CartService

# Define a Blueprint for cart routes
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """
    Endpoint to retrieve a cart by user ID.
    
    Args:
        user_id (int): ID of the user.
    
    Returns:
        JSON response: Cart details if found, otherwise error message.
    """
    cart = CartService.get_cart_by_user_id(user_id)
    if cart:
        return jsonify({
            'id': cart.id,
            'user_id': cart.user_id,
            'subtotal': cart.subtotal,
            'items': [{
                'product_id': item.product_id,
                'quantity': item.quantity,
                'product_name': item.product.name,
                'product_price': item.product.price
        } for item in cart.items]
        }), 200
    return jsonify({'error': 'Cart not found'}), 404

@cart_bp.route('/cart', methods=['POST'])
def create_cart():
    """
    Endpoint to create a new cart.
    
    Request Body:
        JSON object with 'user_id', 'subtotal' (optional)
    
    Returns:
        JSON response: Newly created cart details.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    subtotal = data.get('subtotal', 0.0)
    
    cart = CartService.create_cart(user_id, subtotal)
    return jsonify({
        'id': cart.id,
        'user_id': cart.user_id,
        'subtotal': cart.subtotal,
    }), 201

@cart_bp.route('/cart/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    """
    Endpoint to update an existing cart's subtotal and/or icon URLs.
    
    Args:
        cart_id (int): ID of the cart to update.
    
    Request Body:
        JSON object with 'subtotal'
    
    Returns:
        JSON response: Updated cart details if successful, otherwise error message.
    """
    data = request.get_json()
    subtotal = data.get('subtotal')
    
    cart = CartService.update_cart(cart_id, subtotal)
    if cart:
        return jsonify({
            'id': cart.id,
            'user_id': cart.user_id,
            'subtotal': cart.subtotal,
        }), 200
    return jsonify({'error': 'Cart not found'}), 404

@cart_bp.route('/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    """
    Endpoint to delete a cart by ID.
    
    Args:
        cart_id (int): ID of the cart to delete.
    
    Returns:
        JSON response: Success message if deleted, otherwise error message.
    """
    if CartService.delete_cart(cart_id):
        return jsonify({'message': 'Cart deleted successfully'}), 200
    return jsonify({'error': 'Cart not found'}), 404
