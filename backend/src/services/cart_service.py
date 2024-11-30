from models.cart import Cart, db


class CartService:
    
    
    @staticmethod
    def get_cart_by_user_id(user_id):
        """
        Retrieve the cart for a specific user by user ID.
        
        Args:
            user_id (int): ID of the user.
        
        Returns:
            Cart: Cart object if found, None otherwise.
        """
        return Cart.query.filter_by(user_id=user_id).first()
    
    
    @staticmethod
    def create_cart(user_id, subtotal=0.0):
        """
        Create a new cart for a user with an optional subtotal and icon URLs.
        
        Args:
            user_id (int): ID of the user.
            subtotal (float): Initial subtotal for the cart (default is 0.0).
        
        Returns:
            Cart: The newly created Cart object.
        """
        # create new cart with the user_id and subtotal given
        cart = Cart(user_id=user_id, subtotal=subtotal)
        
        # add to the db
        db.session.add(cart)
        db.session.commit()
        
        return cart


    @staticmethod
    def update_cart(cart_id, subtotal=None):
        """
        Update an existing cart's subtotal and/or icon URLs.
        
        Args:
            cart_id (int): ID of the cart to update.
            subtotal (float, optional): New subtotal value for the cart.
        
        Returns:
            Cart: The updated Cart object if successful, None otherwise.
        """
        # get the cart by its id
        cart = Cart.query.get(cart_id)
        
        # if found update the subtotal, commit to db, and return updated cart
        if cart:
            if subtotal is not None:
                cart.subtotal = subtotal
            db.session.commit()
            return cart
        return None
    
    
    @staticmethod
    def delete_cart(cart_id):
        """
        Delete a cart by its ID.
        
        Args:
            cart_id (int): ID of the cart to delete.
        
        Returns:
            bool: True if the cart was deleted, False if not found.
        """
        # get the cart by its id
        cart = Cart.query.get(cart_id)
        
        # if found delete the cart and return true
        if cart:
            db.session.delete(cart)
            db.session.commit()
            return True
        return False
