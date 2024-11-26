from flask import Blueprint, request, jsonify
from services.cart_item_service import CartItemService

# Define a Blueprint for cart item routes
cart_item_bp = Blueprint('cart_item', __name__)

@cart_item_bp.route('/cart/<int:user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    """
    Endpoint to add a product to the user's cart.
    
    Args:
        user_id (int): ID of the user.
    
    Request Body:
        JSON object with 'product_id' and optional 'quantity' (default is 1)
    
    Returns:
        JSON response: Updated cart details.
    """
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Add the product to the cart using CartItemService
    cart = CartItemService.add_item_to_cart(user_id, product_id, quantity)

    # Return the updated cart details
    return jsonify({
        'id': cart.id,
        'subtotal': cart.subtotal,
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'product_name': item.product.name,
            'product_price': item.product.price
        } for item in cart.items]
    }), 201

@cart_item_bp.route('/cart/<int:cart_id>/remove', methods=['DELETE'])
def remove_from_cart(cart_id):
    """
    Endpoint to remove a product from the cart by cart item ID.
    
    Args:
        cart_id (int): ID of the cart.
    
    Request Body:
        JSON object with 'cart_item_id'
    
    Returns:
        JSON response: Success message if removed, otherwise error message.
    """
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')

    # Remove the item from the cart using CartItemService
    success = CartItemService.remove_item_from_cart(cart_id, cart_item_id)
    
    if success:
        return jsonify({"message": "Item removed successfully"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404
