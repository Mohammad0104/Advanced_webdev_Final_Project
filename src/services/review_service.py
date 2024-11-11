from models.review import Review, db
from datetime import datetime

def add_review(reviewer_id, product_id, rating, explanation):
    new_review = Review(
        reviewer_id=reviewer_id,
        product_id=product_id,
        rating=rating,
        explanation=explanation,
        review_date=datetime.utcnow()  # Use UTC for consistency
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review

def get_reviews_by_product(product_id):
    return Review.query.filter_by(product_id=product_id).all()

def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False
