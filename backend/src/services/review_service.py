from models.review import Review, db
from datetime import datetime


def add_review(reviewer_id, product_id, rating, explanation):
    """Add a new review for a product.

    Args:
        reviewer_id (int): id of the user writing the review.
        product_id (int): id of the product being reviewed.
        rating (float): the rating given to the product (e.g., 1 to 5).
        explanation (str): textual explanation of the review.

    Returns:
        Review: newly created review object.
    """
    # create a new instance of the Review model with the provided data
    new_review = Review(
        reviewer_id=reviewer_id,
        product_id=product_id,  
        rating=rating,   
        explanation=explanation,
        review_date=datetime.utcnow()
    )
    
    # ddd the new review to the db and commit
    db.session.add(new_review)
    db.session.commit()
    
    # return the new review object
    return new_review


def get_reviews_by_product(product_id):
    """ Retrieve all reviews for a given product, including associated user and seller details.

    Args:
        product_id (int): id of the product for which reviews are to be retrieved.

    Returns:
        list[dict]: a list of reviews, each represented as a dict containing:
            - id (int): id of the review.
            - rating (float): rating given in the review.
            - explanation (str): textual explanation of the review.
            - review_date (str): review date in ISO 8601 format.
            - reviewer_name (str): name of the user who wrote the review.
            - seller_id (int): id of the seller of the reviewed product.
            - seller_name (str): name of the seller.
            - product_id (int): id of the reviewed product.
            - product_name (str): name of the reviewed product.

    Raises:
        Exception: if there is an error retrieving reviews from the database.
    """
    try:
        # retrieve all reviews of the given product
        reviews = Review.query.filter_by(product_id=product_id).all()
        
        # format reviews data with product and seller info
        reviews_data = [
            {
                'id': review.id,
                'rating': review.rating,
                'explanation': review.explanation,
                'review_date': review.review_date.isoformat(),
                'reviewer_name': review.reviewing_user.name,
                'seller_id': review.reviewed_product.seller_id,
                'seller_name': review.reviewed_product.seller.name,
                'product_id': review.product_id,
                'product_name': review.reviewed_product.name 
            }
            for review in reviews
        ]
        # return the list
        return reviews_data
    except Exception as e:
        raise Exception(f"Error retrieving reviews: {str(e)}")
    

def delete_review(review_id):
    """Delete a review from the database.

    Args:
        review_id (int): id of the review to be deleted.

    Returns:
        bool: True if the review was successfully deleted, otherwise False.
    """
    # retrieve the review by its ID
    review = Review.query.get(review_id)
    
    # if the review exists, delete it from the database and commit
    if review:
        db.session.delete(review)
        db.session.commit()
        return True
    return False