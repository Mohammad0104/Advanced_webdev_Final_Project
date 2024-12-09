// Review.js
import React, { useState } from 'react';

function Review() {
  const [reviews, setReviews] = useState([]);
  const [reviewText, setReviewText] = useState('');
  const [rating, setRating] = useState(0);

  const handleAddReview = () => {
    if (reviewText.trim() && rating > 0) {
      setReviews([...reviews, { text: reviewText, rating }]);
      setReviewText('');
      setRating(0);
    } else {
      alert('Please add a valid review and rating!');
    }
  };

  return (
    <div>
      <h1>Product Reviews</h1>
      <div>
        <textarea
          placeholder="Write your review..."
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          style={{ width: '100%', height: '80px', marginBottom: '10px' }}
        ></textarea>
        <br />
        <label>
          Rating:
          <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
            <option value={0}>Select Rating</option>
            <option value={1}>1 - Poor</option>
            <option value={2}>2 - Fair</option>
            <option value={3}>3 - Good</option>
            <option value={4}>4 - Very Good</option>
            <option value={5}>5 - Excellent</option>
          </select>
        </label>
        <br />
        <button onClick={handleAddReview} style={{ marginTop: '10px' }}>
          Add Review
        </button>
      </div>
      <div>
        <h2>All Reviews</h2>
        {reviews.length === 0 ? (
          <p>No reviews yet.</p>
        ) : (
          reviews.map((review, index) => (
            <div key={index} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px' }}>
              <p><strong>Review:</strong> {review.text}</p>
              <p><strong>Rating:</strong> {review.rating}/5</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Review;
