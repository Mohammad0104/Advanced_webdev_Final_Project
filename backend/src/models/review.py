from . import db

class Review(db.Model):
    """Database model representing a review

    Attributes:
        id (int): The ID primary key of the review.
        reviewer_id (int): foreign key of the user.id that created the review
        product_id (int): foreign key of the product.id that the review is for
        rating (float): the rating that was given to the product (out of 5)
        explanation (str): the review text (explanation) that the reviewer submitted
        review_date (datetime): the date that the review was submitted
        
        reviewing_user (relationship): relationship to the User model (the user who created this review)
        reviewed_product (relationship): relationship to the Product model (the product that the review is for)
    """
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    explanation = db.Column(db.String(300))
    review_date = db.Column(db.Date, nullable=False)
    
    # relationship to the user who wrote the review
    reviewing_user = db.relationship('User', backref='reviews')
    
    # relationship to the product being reviewed
    reviewed_product = db.relationship('Product', back_populates='reviews')