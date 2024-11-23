from . import db
from .review import Review
from .cart_item import CartItem


class Product(db.Model):
    __tablename__ = 'product'  # Explicitly define the table name for clarity

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
    image = db.Column(db.LargeBinary, nullable=True)  # Allow nullable for optional images
    date_listed = db.Column(db.Date, nullable=False)
    year_product_made = db.Column(db.String(4))
    avg_rating = db.Column(db.Float, default=0.0)  # Default to 0.0 for new products

    # Relationships
    seller = db.relationship('User', backref='products', lazy=True)
    reviews = db.relationship('Review', back_populates='reviewed_product', lazy='dynamic')
    cart_items = db.relationship('CartItem', back_populates='product', lazy='dynamic')

    def to_dict(self):
        """
        Convert the product model to a dictionary representation.
        This is used for serializing the product object into JSON-friendly data.
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
        """
        String representation of the Product object for debugging purposes.
        """
        return f"<Product {self.name} (ID: {self.id})>"
