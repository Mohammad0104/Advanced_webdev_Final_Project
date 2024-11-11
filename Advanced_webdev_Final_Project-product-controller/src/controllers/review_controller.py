from flask import Blueprint, request, jsonify
from services.review_service import add_review, get_reviews_by_product, delete_review

review_blueprint = Blueprint('review', __name__)

@review_blueprint.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    if not data or not all(k in data for k in ('reviewer_id', 'product_id', 'rating', 'explanation')):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        review = add_review(
            reviewer_id=data['reviewer_id'],
            product_id=data['product_id'],
            rating=data['rating'],
            explanation=data['explanation']
        )
        return jsonify(review.id), 201  # Assuming review object has an 'id' attribute
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_blueprint.route('/reviews/product/<int:product_id>', methods=['GET'])
def retrieve_reviews(product_id):
    try:
        reviews = get_reviews_by_product(product_id)
        reviews_data = [{'id': r.id, 'rating': r.rating, 'explanation': r.explanation, 'review_date': r.review_date.isoformat()} for r in reviews]
        return jsonify(reviews_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@review_blueprint.route('/reviews/<int:review_id>', methods=['DELETE'])
def remove_review(review_id):
    try:
        if delete_review(review_id):
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            return jsonify({'message': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
