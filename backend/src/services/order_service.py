from models.order import Order, db
from datetime import datetime

def get_all_orders_by_userid(user_id: int):
    return Order.query.filter_by(user_id=user_id).all()

def get_order_by_id(id: int):
    return Order.query.filter_by(id=id).first()

def create_order(user_id: int, total: float, order_date: datetime):
    """
    Creates a new order in the database.

    Args:
        user_id (int): ID of the user placing the order.
        total (float): total amount of the order.
        order_date (datetime): date and time when ordered

    Returns:
        Order: the created Order object.
    """
    # Create a new order instance
    new_order = Order(
        user_id=user_id,
        total=total,
        order_date=order_date,
    )
    
    # Add the new order to the session and commit
    db.session.add(new_order)
    db.session.commit()

    return new_order