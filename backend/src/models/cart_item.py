from . import db

class CartItem(db.Model):
    """Database model representing a cartitem

    Attributes:
        id (int): The ID primary key of the cartitem.
        cart_id (int): foreign key of the cart.id that this cartitem is apart of
        product_id (int): foreign key of the product.id that this cartitem is associated with
        quantity (int): the amount of this cartitem that is in the associated cart
        
        cart (relationship): relationship to the Cart model (the cart that this cartitem is apart of)
        product (relationship): relationship to the Product model (the product that this cartitem is associated with)
    """
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    
    cart = db.relationship('Cart', backref='items')
    product = db.relationship('Product', back_populates='cart_items')