from . import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.String(300))
    review_date = db.Column(db.Date, nullable=False)
    
    reviewing_user = db.relationship('User', backref='reviews')
    reviewed_product = db.relationship('Product', backref='reviews')