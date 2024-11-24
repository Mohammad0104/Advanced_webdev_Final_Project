from flask import Blueprint, request, jsonify
from services.review_service import add_review, get_reviews_by_product, delete_review

# Create a Flask Blueprint named 'review' for review-related routes
review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/reviews', methods=['POST'])
def create_review():
    """
    Route to create a new review for a product.
    Expects JSON payload with reviewer_id, product_id, rating, and explanation.
    """
    data = request.get_json()

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
            rating=int(data['rating']),  # Ensure rating is an integer
            explanation=str(data['explanation'])  # Ensure explanation is a string
        )
        # Return success response
        return jsonify({'id': review.id, 'message': 'Review created successfully'}), 201
    except ValueError:
        return jsonify({'message': 'Invalid data format. Rating must be an integer.'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create review: {str(e)}'}), 500


@review_blueprint.route('/reviews/product/<int:product_id>', methods=['GET'])
def retrieve_reviews(product_id):
    """
    Route to retrieve all reviews for a specific product.
    """
    try:
        # Fetch reviews from the service
        reviews = get_reviews_by_product(product_id)

        if not reviews:
            return jsonify({'message': 'No reviews found for this product'}), 404

        # Format reviews into JSON response
        reviews_data = [
            {
                'id': r.id,
                'rating': r.rating,
                'explanation': r.explanation,
                'review_date': r.review_date.isoformat()
            }
            for r in reviews
        ]
        return jsonify({'reviews': reviews_data}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve reviews: {str(e)}'}), 500


@review_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
def remove_review(review_id):
    """
    Route to delete a review by its ID.
    """
    try:
        # Attempt to delete the review
        if delete_review(review_id):
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            return jsonify({'message': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete review: {str(e)}'}), 500
