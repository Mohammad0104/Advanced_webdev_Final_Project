from flask import Blueprint, request, jsonify
from services.cart_service import CartService
from services.cart_item_service import CartItemService
from models.cart import Cart, db
from sqlalchemy.exc import SQLAlchemyError

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


@cart_bp.route('/cart/<int:cart_id>', methods=['PUT', 'OPTIONS'])
def update_cart(cart_id):
    """
    Endpoint to update an existing cart's subtotal and cart item quantities.
    
    Args:
        cart_id (int): ID of the cart to update.
    
    Request Body:
        JSON object with 'product_id' and 'quantity' for a specific cart item.
    
    Returns:
        JSON response: Updated cart details if successful, otherwise error message.
    """
    data = request.get_json()
    product_id = data.get('product_id')  # Product ID for the cart item
    quantity = data.get('quantity')


    if product_id is None or quantity is None:
        return jsonify({'error': 'Product ID and quantity are required'}), 400
    
    
    # Find the cart
    cart = Cart.query.get(cart_id)
    
    cart_item = next((item for item in cart.items if item.product_id == product_id), None)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    try:
        # Call the CartItemService to update the item and recalculate the subtotal
        CartItemService.update_item_and_cart(cart, cart_item.id, quantity)
        
        return jsonify({
            'id': cart.id,
            'subtotal': cart.subtotal,
            'items': [{
                'product_id': item.product_id,
                'quantity': item.quantity,
                'product_name': item.product.name,
                'product_price': item.product.price,
            } for item in cart.items]
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred: ' + str(e)}), 500


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
