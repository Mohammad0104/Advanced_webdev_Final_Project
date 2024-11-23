import React, { useState, useEffect } from 'react';

function Review({ productId }) {
  const [reviews, setReviews] = useState([]);
  const [reviewText, setReviewText] = useState('');
  const [rating, setRating] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch reviews from the backend
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:8080/product/${productId}/reviews`);
        if (!response.ok) {
          throw new Error('Failed to fetch reviews');
        }
        const data = await response.json();
        setReviews(data.reviews);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchReviews();
  }, [productId]);

  const handleAddReview = async () => {
    if (reviewText.trim() && rating > 0) {
      try {
        const newReview = { review_text: reviewText, rating };
        const response = await fetch(`http://localhost:8080/product/${productId}/reviews`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newReview),
        });

        if (!response.ok) {
          throw new Error('Failed to add review');
        }

        const data = await response.json();
        setReviews([...reviews, data.review]); // Add the new review to the list
        setReviewText(''); // Clear input fields
        setRating(0);
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert('Please add a valid review and rating!');
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '10px' }}>
      <h1 style={{ textAlign: 'center' }}>Product Reviews</h1>
      <div style={{ marginBottom: '20px' }}>
        <textarea
          placeholder="Write your review..."
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          style={{ width: '100%', height: '80px', marginBottom: '10px', borderRadius: '5px', padding: '10px', border: '1px solid #ccc' }}
        ></textarea>
        <br />
        <label>
          <strong>Rating:</strong>
          <select
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
            style={{ marginLeft: '10px', padding: '5px', borderRadius: '5px', border: '1px solid #ccc' }}
          >
            <option value={0}>Select Rating</option>
            <option value={1}>1 - Poor</option>
            <option value={2}>2 - Fair</option>
            <option value={3}>3 - Good</option>
            <option value={4}>4 - Very Good</option>
            <option value={5}>5 - Excellent</option>
          </select>
        </label>
        <br />
        <button
          onClick={handleAddReview}
          style={{
            marginTop: '10px',
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Add Review
        </button>
      </div>
      <div>
        <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>All Reviews</h2>
        {loading ? (
          <p>Loading reviews...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : reviews.length === 0 ? (
          <p>No reviews yet.</p>
        ) : (
          reviews.map((review) => (
            <div key={review.id} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px', borderRadius: '5px' }}>
              <p>
                <strong>Review:</strong> {review.review_text}
              </p>
              <p>
                <strong>Rating:</strong> {review.rating}/5
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Review;
