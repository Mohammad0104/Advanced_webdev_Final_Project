from . import db

class Cart(db.Model):
    """Database model representing a user's shopping cart
    
    Has a foreign key of the user.id (`user_id`) which represents the user who created the cart

    Attributes:
        id (int): primary key identifier for the cart.
        user_id (int): foreign key referencing the user who owns this cart.
        subtotal (float): total cost of all items in the cart.
        user (relationship): relationship to the User model with backref to cart.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subtotal = db.Column(db.Float)
    
    user = db.relationship('User', backref='cart')