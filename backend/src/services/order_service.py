from models.order import Order, db
from models.cart import Cart
from models.order_item import OrderItem
from datetime import datetime


def get_all_orders_by_userid(user_id: int):
    """Retrieves all orders associated with a specific user.

    Args:
        user_id (int): id of the user.

    Returns:
        List[Order]: list of orders belonging to the user.

    Raises:
        Exception: if an error occurs during the database query.
    """
    try:
        orders = Order.query.filter_by(user_id=user_id).all()
        return orders
    except Exception as e:
        print(f"Error in get_all_orders_by_userid: {e}")
        raise


def get_order_by_id(id: int):
    """Retrieves a single order by its id.

    Args:
        id (int): id of the order.

    Returns:
        Order: the order object if found, otherwise None.
    """
    return Order.query.filter_by(id=id).first()


def create_order(user_id: int):
    """Creates a new order for the user by transferring items from their cart to the order.

    Args:
        user_id (int): id of the user for whom the order is created.

    Returns:
        Order: the newly created order object.

    Raises:
        ValueError: if the cart is not found, has no items, or if there is insufficient stock.
        Exception: for any other issues during the process.
    """
    try:
        print("Fetching cart for user_id:", user_id)
        
        # get the cart for the given user
        cart = Cart.query.filter_by(user_id=user_id).first()
        
        # if the cart isn't found
        if not cart:
            raise ValueError("Cart not found")

        print("Cart found. Subtotal:", cart.subtotal)

        # ensure cart items are accessible
        if not cart.items:
            raise ValueError("Cart has no items")
        
    
        # create a new order with the given information
        new_order = Order(
            user_id=user_id,
            total=cart.subtotal,
            order_date=datetime.utcnow()
        )
        
        # add and commit changes to the db
        db.session.add(new_order)
        db.session.commit()


        # transfer items from cart to order
        for cart_item in cart.items:
            # get product from cart_item using the relationship
            product = cart_item.product
            
            # if the product isn't found
            if not product:
                raise ValueError(f"Product with ID {cart_item.product_id} not found.")

            # if the product quantity is less than the cart_item quantity
            if product.quantity < cart_item.quantity:
                raise ValueError(
                    f"Insufficient stock for product {product.name}. "
                    f"Available: {product.quantity}, Requested: {cart_item.quantity}"
                )

            # create an order item and add to db
            print(f"Adding item to order: {product.name}, Quantity: {cart_item.quantity}, Price: {product.price}")
            order_item = OrderItem(
                order_id=new_order.id,
                product_name=product.name,
                quantity=cart_item.quantity,
                price=product.price
            )
            db.session.add(order_item)

            # update product quantity
            product.quantity -= cart_item.quantity
            if product.quantity == 0:
                print(f"Product {product.name} is now out of stock.")

            # delete the cart item from the db
            db.session.delete(cart_item)

        # delete the cart from the db and commit the changes
        db.session.delete(cart)
        db.session.commit()
        
        # return the new order
        print("Order created successfully")
        return new_order
    except Exception as e:
        print("Error in create_order:", str(e))
        db.session.rollback() # rollback the db changes
        raise  # reraise the exception for better error handling
