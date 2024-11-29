from . import db

class Order(db.Model):
    """Database model representing an order

    Attributes:
        id (int): The ID primary key of the order.
        user_id (int): foreign key of the user.id that created the order
        total (float): order total price
        order_date (datetime): the date the order was made
        
        user (relationship): relationship to the User model (the user who created this order)
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    
    user = db.relationship('User', backref='orders')
    
    
    def to_dict(self):
        """Convert order object into a dictionary

        Returns:
            dict: dict of the order object (also includes information with the associated order_items)
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'order_date': self.order_date.isoformat(),
            'items': [
                {
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                }
                for item in self.order_items  # Accessing the relationship to OrderItem
            ]
        }