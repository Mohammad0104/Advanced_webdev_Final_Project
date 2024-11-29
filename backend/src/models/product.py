from . import db
from .review import Review
from .cart_item import CartItem


class Product(db.Model):
    """Database model representing a product

    Attributes:
        id (int): id primary key of the product
        seller_id (int): The ID of the seller listing the product.
        name (str): Name of the product.
        description (str): Description of the product.
        price (float): Price of the product.
        gender (str): Target gender for the product.
        size (str): Size of the product.
        youth_size (bool): Whether the product is a youth size.
        featured (bool): Whether the product is featured.
        brand (str): Brand of the product.
        sport (str): Associated sport for the product.
        quantity (int): Quantity of the product available.
        condition (str): Condition of the product.
        image (bytes): Image of the product.
        date_listed (datetime): Date the product was listed.
        year_product_made (str): Year the product was made.
        avg_rating (float): Average rating of the product.
        
        seller (relationship): relationship to the User model (the user who is selling this product)
        review (relationship): relationship to the Review model (the reviews that are of this product)
        cart_items (relationship): relationship to the CartItem model (the cart items that are linked to this product)
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    youth_size = db.Column(db.Boolean, nullable=False)
    featured = db.Column(db.Boolean, default=False, nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    sport = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    condition = db.Column(db.String(30), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)  # allow nullable for optional images
    date_listed = db.Column(db.Date, nullable=False)
    year_product_made = db.Column(db.String(4))
    avg_rating = db.Column(db.Float, default=0.0)  # default to 0.0 for new products

    # relationships
    seller = db.relationship('User', backref='products', lazy=True)
    reviews = db.relationship('Review', back_populates='reviewed_product', lazy='dynamic')
    cart_items = db.relationship('CartItem', back_populates='product', lazy='dynamic')


    def to_dict(self):
        """Convert product object into a dictionary

        Returns:
            dict: dict of the product object
        """
        product_dict = {
            'id': self.id,
            'seller_id': self.seller_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'gender': self.gender,
            'size': self.size,
            'youth_size': self.youth_size,
            'featured': self.featured,
            'brand': self.brand,
            'sport': self.sport,
            'quantity': self.quantity,
            'condition': self.condition,
            'image': self.image,  # This will be base64-encoded at the API level
            'date_listed': self.date_listed.isoformat() if self.date_listed else None,
            'year_product_made': self.year_product_made,
            'avg_rating': self.avg_rating,
        }

        return product_dict


    def __repr__(self):
        """String representation of the Product object for debugging purposes.

        Returns:
            str: string representation of the Product object
        """
        return f"<Product {self.name} (ID: {self.id})>"
