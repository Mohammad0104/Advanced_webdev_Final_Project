from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    image_url = db.Column(db.String(200), nullable=False)
    date_listed = db.Column(db.Date, nullable=False)
    year_product_made = db.Column(db.String(4))
    avg_rating = db.Column(db.Float)
    
    seller = db.relationship('User', backref='products') 
    reviews = db.relationship('Review', backref='reviewed_product')
    cart_items = db.relationship('CartItem', backref='product')
    