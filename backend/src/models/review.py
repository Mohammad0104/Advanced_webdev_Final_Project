from . import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    explanation = db.Column(db.String(300))
    review_date = db.Column(db.Date, nullable=False)
    
    # relationship to the user who wrote the review
    reviewing_user = db.relationship('User', backref='reviews')
    
    # relationship to the product being reviewed
    # reviewed_product = db.relationship('Product', backref='reviews')
    # reviewed_product = db.relationship('Product', back_populates='product_reviews')
    reviewed_product = db.relationship('Product', back_populates='reviews')