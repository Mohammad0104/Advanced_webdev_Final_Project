from flask import Blueprint, request, jsonify
from services.review_service import add_review, get_reviews_by_product, delete_review


# blueprint for review-related routes
review_blueprint = Blueprint('review', __name__)


@review_blueprint.route('/create_review', methods=['POST'])
def create_review():
    """Endpoint to create a new review

    Returns:
        JSON: JSON message with the review id or error message
    """
    data = request.get_json()
    
    print(data)

    # Validate required fields
    required_fields = ('reviewer_id', 'product_id', 'rating', 'explanation')
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    try:
        # Add the review using the service
        review = add_review(
            reviewer_id=data['reviewer_id'],
            product_id=data['product_id'],
            rating=float(data['rating']),  # Ensure rating is a float
            explanation=str(data['explanation'])  # Ensure explanation is a string
        )
        # Return success response
        return jsonify({'id': review.id, 'message': 'Review created successfully'}), 201
    except ValueError:
        return jsonify({'message': 'Invalid data format. Rating must be an integer.'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create review: {str(e)}'}), 500


@review_blueprint.route('/reviews/product/<int:product_id>', methods=['GET'])
def retrieve_reviews(product_id: int):
    """Endpoint to get all the reviews for a given product

    Args:
        product_id (int): the id of the product to get all the reviews for

    Returns:
        JSON: JSON message with a list of reviews or error message
    """
    try:
        # Fetch reviews from the service
        reviews = get_reviews_by_product(product_id)
        
        print(reviews)

        if not reviews:
            return jsonify({'reviews': [], 'message': 'No reviews yet for this product'}), 200
        
        return jsonify({'reviews': reviews}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve reviews: {str(e)}'}), 500


@review_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
def remove_review(review_id: int):
    """Endpoint to delete a review

    Args:
        review_id (int): the id of the review to delete

    Returns:
        JSON: JSON success or failure message
    """
    try:
        # Attempt to delete the review
        if delete_review(review_id):
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            return jsonify({'message': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete review: {str(e)}'}), 500
