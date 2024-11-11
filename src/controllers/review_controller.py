from flask import Blueprint, request, jsonify
from services.review_service import add_review, get_reviews_by_product, delete_review

# Create a Flask Blueprint named 'review'. This allows the routes to be organized and registered in a modular way.
review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/reviews', methods=['POST'])
def create_review():
    # Get JSON data from the HTTP request
    data = request.get_json()
    # Validate that the necessary fields are present in the data
    if not data or not all(k in data for k in ('reviewer_id', 'product_id', 'rating', 'explanation')):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        # Call the service function to add a new review to the database
        review = add_review(
            reviewer_id=data['reviewer_id'],
            product_id=data['product_id'],
            rating=data['rating'],
            explanation=data['explanation']
        )
        # Return the ID of the new review with a 201 CREATED status
        return jsonify(review.id), 201
    except Exception as e:
        # If an error occurs, return an error message with a 500 INTERNAL SERVER ERROR status
        return jsonify({'error': str(e)}), 500

@review_blueprint.route('/reviews/product/<int:product_id>', methods=['GET'])
def retrieve_reviews(product_id):
    try:
        # Retrieve reviews based on the product_id
        reviews = get_reviews_by_product(product_id)
        # Format the reviews data for the response
        reviews_data = [
            {'id': r.id, 'rating': r.rating, 'explanation': r.explanation, 'review_date': r.review_date.isoformat()}
            for r in reviews
        ]
        # Return the formatted reviews data with a 200 OK status
        return jsonify(reviews_data), 200
    except Exception as e:
        # If an error occurs, return an error message with a 500 INTERNAL SERVER ERROR status
        return jsonify({'error': str(e)}), 500

@review_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
def remove_review(review_id):
    try:
        # Attempt to delete the review by its ID
        if delete_review(review_id):
            # If successful, return a success message with a 200 OK status
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            # If no review is found with the given ID, return a not found message with a 404 NOT FOUND status
            return jsonify({'message': 'Review not found'}), 404
    except Exception as e:
        # If an error occurs during the deletion process, return an error message with a 500 INTERNAL SERVER ERROR status
        return jsonify({'error': str(e)}), 500
