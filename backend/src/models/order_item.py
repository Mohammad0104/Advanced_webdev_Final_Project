from . import db

class OrderItem(db.Model):
    """Database model representing an orderitem

    Attributes:
        id (int): The ID primary key of the orderitem.
        order_id (int): foreign key of the order.id that this orderitem is apart of
        product_name (str): the name of the product associated with the orderitem (at the time it was ordered)
        quantity (int): the amount of this orderitem that is apart of the order
        price (float): the price of each of this orderitem
        
        order (relationship): relationship to the Order model (the order that this orderitem is apart of)
    """
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', backref='order_items')