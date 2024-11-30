from models.cart_item import CartItem, db
from models.cart import Cart
from services.cart_service import CartService
from sqlalchemy.exc import SQLAlchemyError


class CartItemService:


    @staticmethod
    def add_item_to_cart(user_id, product_id, quantity=1):
        """Adds cart item to the given user's cart.
        If the cart item already exists in the cart, then the quantity
        of it is increased by 1

        Args:
            user_id (int): id of the user
            product_id (int): id of the product to add to the cart
            quantity (int, optional): quantity of the product to add. Defaults to 1.

        Returns:
            Cart: The updated cart object
        """
        # retrieve the user's cart wth CartService
        cart = CartService.get_cart_by_user_id(user_id)
        
        # if no cart exists for the user, create a new one
        if not cart:
            cart = CartService.create_cart(user_id)


        # check if the product already exists in the cart (if a cartitem linked to the product exists)
        existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        
        # if the item already exists in the cart, increase the quantity
        if existing_item:
            existing_item.quantity += quantity
        else:
            # otherwise, create a new cart item
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)


        # update the cart's subtotal after adding/updating the item
        CartItemService._update_cart_subtotal(cart)

        # commit changes to the db
        db.session.commit()
        
        # return the updated cart
        return cart


    @staticmethod
    def remove_item_from_cart(cart_id, cart_item_id):
        """Removes an item from the cart.

        Args:
            cart_id (int): id of the cart.
            cart_item_id (int): id of the cart item to remove.

        Returns:
            Cart: The updated cart object, or None if the cart item is not found
        """
        
        # find the cart item by it's id
        cart_item = CartItem.query.filter_by(id=cart_item_id).first()
        
        if cart_item:
            # delete the cart item from the database
            db.session.delete(cart_item)
            db.session.commit()

            # recalculate the cart's subtotal after removal
            cart = Cart.query.get(cart_id)
            if cart:
                # recalculate subtotal by summing up the product of quantity and price for each item
                cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)
                
                # commit changes to the db
                db.session.commit()

            # return the updated cart object
            return cart

        # return None if the cart item is not found
        return None
            
            
    @staticmethod
    def update_item_and_cart(cart, item_id, new_quantity):
        """Updates the quantity of a specific item in the cart or removes the item if quantity is zero.

        Args:
            cart (Cart): the cart object.
            item_id (int): the ID of the cart item to update.
            new_quantity (int): the new quantity for the cart item.

        Raises:
            ValueError: if the cart item is not found or the requested quantity exceeds stock.
            RuntimeError: if a database error occurs.

        Returns:
            None
        """
        # find the cart item, from the given cart object if it exists
        cart_item = next((item for item in cart.items if item.id == item_id), None)
        
        # if the cart item is not found in the given cart
        if not cart_item:
            raise ValueError(f"Cart item with ID {item_id} not found.")
        

        # if the new quantity exceeds the product quantity
        if new_quantity > cart_item.product.quantity:
            raise ValueError(f"Only {cart_item.product.quantity} units of {cart_item.product.name} are available.")


        # update the quantity or remove the item if quantity is zero
        if new_quantity == 0:
            cart.items = [item for item in cart.items if item.id != item_id]
        else:
            cart_item.quantity = new_quantity
            
            
        # recalculate the subtotal
        cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)


        # commit the changes to the db
        try:
            db.session.add(cart)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError("Database error occurred: " + str(e))

        
    @staticmethod
    def _update_cart_subtotal(cart):
        """Updates the subtotal of the cart based on its cart items.

        Args:
            cart (Cart): the cart object to update.

        Returns:
            None
        """
        # calculate the subtotal by summing up the product of quantity and price for each item
        cart.subtotal = sum(item.quantity * item.product.price for item in cart.items)
        
        # add to the db
        db.session.add(cart)
