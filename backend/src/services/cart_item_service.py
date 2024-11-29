from models.cart_item import CartItem, db
from models.cart import Cart
from services.cart_service import CartService
from sqlalchemy.exc import SQLAlchemyError

class CartItemService:

    @staticmethod
    def add_item_to_cart(user_id, product_id, quantity=1):
        # Step 1: Retrieve the user's cart (1use CartService to get the cart)
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
        cart_item = CartItem.query.filter_by(id=cart_item_id).first()
        if cart_item:
            # Step 2: Delete the cart item from the database
            db.session.delete(cart_item)
            db.session.commit()

            # Step 3: Recalculate the cart's subtotal after removal
            cart = Cart.query.get(cart_id)
            if cart:
                # Recalculate the subtotal by summing up the product of quantity and price for each item
                cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)
                db.session.commit()  # Commit the subtotal update

            return cart  # Return the updated cart object

        return None  # If the cart item is not found
            
    @staticmethod
    def update_item_and_cart(cart, item_id, new_quantity):
        # Find the cart item
        cart_item = next((item for item in cart.items if item.id == item_id), None)
        
        if not cart_item:
            raise ValueError(f"Cart item with ID {item_id} not found.")
        

        # Check the product's available stock
        if new_quantity > cart_item.product.quantity:
            raise ValueError(f"Only {cart_item.product.quantity} units of {cart_item.product.name} are available.")

        # Update the quantity or remove the item if quantity is zero
        if new_quantity == 0:
            cart.items = [item for item in cart.items if item.id != item_id]
        else:
            cart_item.quantity = new_quantity
            
        # Recalculate the subtotal
        cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)

        # Commit the changes to the database
        try:
            db.session.add(cart)
            db.session.commit()
            print('yoyoy')
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError("Database error occurred: " + str(e))

        
    @staticmethod
    def _update_cart_subtotal(cart):
        # Calculate the subtotal by summing up the product of quantity and price for each item
        cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)
        db.session.add(cart)
