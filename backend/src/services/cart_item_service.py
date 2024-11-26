from models.cart_item import CartItem, db
from services.cart_service import CartService

class CartItemService:

    @staticmethod
    def add_item_to_cart(user_id, product_id, quantity=1):
        # Step 1: Retrieve the user's cart (use CartService to get the cart)
        cart = CartService.get_cart_by_user_id(user_id)
        if not cart:
            # If no cart exists for the user, create a new one
            cart = CartService.create_cart(user_id)

        # Step 2: Check if the product already exists in the cart
        existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if existing_item:
            # If the item already exists in the cart, increase the quantity
            existing_item.quantity += quantity
        else:
            # Otherwise, create a new cart item
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        # Step 3: Update the cart's subtotal after adding/updating the item
        CartItemService._update_cart_subtotal(cart)

        db.session.commit()
        return cart

    @staticmethod
    def remove_item_from_cart(cart_id, cart_item_id):
        # Step 1: Find the cart item to remove
        cart_item = CartItem.query.filter_by(id=cart_item_id, cart_id=cart_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.comm
            
    @staticmethod
    def _update_cart_subtotal(cart):
        # Calculate the subtotal by summing up the product of quantity and price for each item
        cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)
        db.session.add(cart)
