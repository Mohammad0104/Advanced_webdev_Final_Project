import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function PaymentSuccessPage() {
  const navigate = useNavigate();

  // Example userId, you can get this from your app's state or props
  const userId = 123; // Replace with actual logic to fetch user ID

  // Function to navigate to the order page
  const redirectToOrderPage = () => {
    navigate(`/orders/${userId}`);
  };

  return (
    <div className="payment-success">
      <h1>Payment Successful!</h1>
      <p>Your payment was processed successfully.</p>
      <button onClick={redirectToOrderPage}>View My Orders</button>
    </div>
  );
}
