from .models.cart_model import Cart
from . import db

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
    def create_cart(user_id, subtotal=0.0, icon_urls=""):
        """
        Create a new cart for a user with an optional subtotal and icon URLs.
        
        Args:
            user_id (int): ID of the user.
            subtotal (float): Initial subtotal for the cart (default is 0.0).
            icon_urls (str): String of icon URLs associated with the cart.
        
        Returns:
            Cart: The newly created Cart object.
        """
        cart = Cart(user_id=user_id, subtotal=subtotal, icon_urls=icon_urls)
        db.session.add(cart)
        db.session.commit()
        return cart

    @staticmethod
    def update_cart(cart_id, subtotal=None, icon_urls=None):
        """
        Update an existing cart's subtotal and/or icon URLs.
        
        Args:
            cart_id (int): ID of the cart to update.
            subtotal (float, optional): New subtotal value for the cart.
            icon_urls (str, optional): New icon URLs to associate with the cart.
        
        Returns:
            Cart: The updated Cart object if successful, None otherwise.
        """
        cart = Cart.query.get(cart_id)
        if cart:
            if subtotal is not None:
                cart.subtotal = subtotal
            if icon_urls is not None:
                cart.icon_urls = icon_urls
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
        cart = Cart.query.get(cart_id)
        if cart:
            db.session.delete(cart)
            db.session.commit()
            return True
        return False
