from models.review import Review, db
from datetime import datetime

def add_review(reviewer_id, product_id, rating, explanation):
    # Create a new instance of the Review model with the provided data
    new_review = Review(
        reviewer_id=reviewer_id,  # ID of the user writing the review
        product_id=product_id,    # ID of the product being reviewed
        rating=rating,            # Numerical rating given to the product
        explanation=explanation,  # Textual explanation of the review
        review_date=datetime.utcnow()  # Current time in UTC as the review date
    )
    # Add the new review to the database session
    db.session.add(new_review)
    # Commit the session to save the review to the database
    db.session.commit()
    # Return the new review object
    return new_review

def get_reviews_by_product(product_id):
    # Retrieve all reviews from the database that match the specified product ID
    return Review.query.filter_by(product_id=product_id).all()

def delete_review(review_id):
    # Retrieve the review by its ID
    review = Review.query.get(review_id)
    if review:
        # If the review exists, delete it from the database
        db.session.delete(review)
        # Commit the transaction to apply the deletion
        db.session.commit()
        return True  # Return True to indicate successful deletion
    return False  # Return False if no review was found to delete