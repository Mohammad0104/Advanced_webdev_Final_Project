import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { checkLoginStatus, get_user_info, redirectTo } from './services/authService';
import ReactStars from 'react-stars';
import { BACKEND_BASE_URL, FRONTEND_BASE_URL } from './constants';

function Review() {
  const navigate = useNavigate();
  const location = useLocation();

  const { productId } = useParams();

  const [reviews, setReviews] = useState([]);
  const [reviewText, setReviewText] = useState('');
  const [rating, setRating] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sellerId, setSellerId] = useState(null);

  // Function to check login status and user info
  const checkUserLoginStatus = async () => {
    const isLoggedIn = await checkLoginStatus(navigate);
    if (isLoggedIn) {
      const userInfo = await get_user_info();
      console.log(userInfo);
      setSellerId(userInfo.id); // Assign this to a product or something else
    } else {
        console.log('User not logged in. Redirecting...');
        redirectTo(`/authorize?next=${FRONTEND_BASE_URL}${location.pathname}`);
    }
  };

  const fetchReviews = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BACKEND_BASE_URL}/reviews/product/${productId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch reviews');
      }
      const data = await response.json();
      console.log(data);
      setReviews(data.reviews);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Fetch reviews from the backend
  useEffect(() => {
    checkUserLoginStatus();
    fetchReviews();
  }, [productId]);

  const handleAddReview = async () => {
    if (reviewText.trim() && rating > 0) {
      try {
        const newReview = { 
          explanation: reviewText, 
          rating , 
          product_id: productId, 
          reviewer_id: sellerId};
        const response = await fetch(`${BACKEND_BASE_URL}/create_review`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newReview),
        });

        if (!response.ok) {
          throw new Error('Failed to add review');
        }

        const data = await response.json();

        const createdReview = {
          id: data.id, // From the backend response
          explanation: reviewText, // Local review text
          rating: rating, // Local rating
          product_id: productId,
          reviewer_id: sellerId, // This can be dynamic if you have user authentication
        };

        setReviews([...reviews, createdReview]); // Add the new review to the list
        alert('Review created successfully!');
        setReviewText(''); // Clear input fields
        setRating(0);
        fetchReviews();
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert('Please add a valid review and rating!');
    }
  };


  return (
    <div style={{ maxWidth: '900px', margin: '20px auto', padding: '20px', borderRadius: '10px', backgroundColor: '#d3d3d3' }}>
      <h1 style={{ textAlign: 'center', fontWeight: 'normal' }}>
        Write a Review for{' '}
        {reviews.length > 0 ? (
          <strong>{reviews[0].product_name}</strong>
        ) : (
          <span>this product</span>
        )}
      </h1>
      {reviews.length > 0 && <p><strong>Seller:</strong> {reviews[0].seller_name}</p>}

      <div style={{ marginBottom: '20px' }}>
        <textarea
          placeholder="Write your review..."
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          style={{ width: '90%', height: '80px', marginBottom: '10px', borderRadius: '5px', padding: '10px', border: '1px solid black', backgroundColor: '#d3d3d3' }}
        ></textarea>
        <br />
        <label>
          <strong>Rating:</strong>
          <div style={{ marginLeft: '10px', display: 'flex', justifyContent: 'center', color: 'black'}}>
            <ReactStars
                count={5} // Total number of stars
                value={rating} // Current rating value
                onChange={setRating} // Callback to update the rating
                size={60} // Size of the stars
                color2={'gold'} // Color for filled stars (gold)
                color1={'#A0A0A0'} // Color for empty stars (light gray)
                half={true} // Allow half stars
            />
          </div>
        </label>
        <br />
        <button
          onClick={handleAddReview}
          style={{
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
      <div style={{ borderRadius: '5px', padding: '10px', marginTop: '80px', backgroundColor: '#333'}}>
        <div>
          <h2 style={{ textAlign: 'center', marginBottom: '0px', color: 'white', fontWeight: 'normal' }}>
            {reviews.length > 0 ? (
              `All Reviews for ${reviews[0].product_name}`
            ) : (
              "No reviews yet for this product"
            )}
          </h2>
          <p style={{color: '#C0C0C0', marginBottom: '50px', fontSize: 'small'}}>If reviews are not loading, refresh page</p>
          {loading ? (
              <p>Loading reviews...</p>
            ) : error ? (
              <p style={{ color: 'red' }}>{error}</p>
            ) : reviews.length === 0 ? (
              <p>No reviews yet for this product.</p>
            ) : (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            {reviews.map((review, index) => (
              <div key={review.id} 
              style={{ 
                 padding: '10px', 
                 marginBottom: '20px', 
                 borderRadius: '5px',
                 backgroundColor: index % 2 === 0 ? '	#B0B0B0' : '#888888',
                 maxWidth: '75%',
                 width: '100%',
                 textAlign: 'center'
              }}>
                <p>
                  <strong>Review:</strong> {review.explanation}
                </p>
                <div>
                  <strong>Rating:</strong>
                  <div style={{ marginLeft: '10px', display: 'flex', justifyContent: 'center' }}>
                    <ReactStars
                      className="bold-stars"
                      count={5} // Total number of stars
                      value={review.rating} // Current rating value
                      size={30} // Size of the stars
                      color2={'gold'} // Color for filled stars (gold)
                      color1={'#333'} // Color for empty stars (light gray)
                      half={true} // Allow half stars
                      edit={false}
                    />
                  </div>
                </div>
                <p>
                  <strong>Reviewer:</strong> {review.reviewer_name}
                </p>
              </div>
            ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Review;
