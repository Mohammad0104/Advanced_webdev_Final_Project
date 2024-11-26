from models.order import Order, db
from models.cart import Cart
from models.order_item import OrderItem
from datetime import datetime

def get_all_orders_by_userid(user_id: int):
    try:
        orders = Order.query.filter_by(user_id=user_id).all()
        return orders
    except Exception as e:
        print(f"Error in get_all_orders_by_userid: {e}")
        raise

def get_order_by_id(id: int):
    return Order.query.filter_by(id=id).first()

# def create_order(user_id: int):
#     print("YO")
#     # Fetch the cart for the user
#     cart = Cart.query.filter_by(user_id=user_id).first()
    
#     print(cart.subtotal)
#     if not cart:
#         raise ValueError("Cart not found")
    
#     # Create a new order
#     new_order = Order(
#         user_id=user_id,
#         total=cart.subtotal,
#         order_date=datetime.utcnow()
#     )
#     db.session.add(new_order)
#     db.session.commit()  # Save the order to get its ID

#     # Transfer items from cart to order
#     for cart_item in cart.items:
#         order_item = OrderItem(
#             order_id=new_order.id,
#             product_name=cart_item.product.name,  
#             quantity=cart_item.quantity,
#             price=cart_item.product.price  
#         )
#         db.session.add(order_item)
#         db.session.delete(cart_item)
    
#     # Delete the cart and its items
#     db.session.delete(cart)
#     db.session.commit()
    
#     return new_order

def create_order(user_id: int):
    try:
        print("Fetching cart for user_id:", user_id)
        cart = Cart.query.filter_by(user_id=user_id).first()
        
        if not cart:
            raise ValueError("Cart not found")

        print("Cart found. Subtotal:", cart.subtotal)

        # Ensure cart items are accessible
        if not cart.items:
            raise ValueError("Cart has no items")

        # Create a new order
        new_order = Order(
            user_id=user_id,
            total=cart.subtotal,
            order_date=datetime.utcnow()
        )
        db.session.add(new_order)
        db.session.commit()  # Save the order to get its ID

        # Transfer items from cart to order
        for cart_item in cart.items:
            print(f"Adding item to order: {cart_item.product.name}, Quantity: {cart_item.quantity}, Price: {cart_item.product.price}")
            order_item = OrderItem(
                order_id=new_order.id,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
            db.session.delete(cart_item)

        # Delete the cart
        db.session.delete(cart)
        db.session.commit()
        
        print("Order created successfully")
        return new_order
    except Exception as e:
        print("Error in create_order:", str(e))
        db.session.rollback()
        raise  # Reraise the exception for better error handling