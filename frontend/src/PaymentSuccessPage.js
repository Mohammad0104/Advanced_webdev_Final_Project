import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FRONTEND_BASE_URL } from './constants';

export default function PaymentSuccessPage() {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  // Example userId, you can get this from your app's state or props
  const userId = 2; // Replace with actual logic to fetch user ID

  useEffect(() => {
    const createOrder = async () => {
      try {
        const response = await fetch(`${FRONTEND_BASE_URL}/orders/create/${userId}`, {
          method: 'POST',
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Order created:', data);
        } else {
          throw new Error('Failed to create order');
        }
      } catch (error) {
        console.error('Error creating order:', error);
        setMessage('Failed to create order. Please try again.');
      }
    };

    createOrder();
  }, [navigate, userId]); // Dependencies to ensure it runs only when `navigate` or `userId` changes

  // Function to navigate to the order page
  const redirectToOrderPage = () => {
    navigate(`/orders/${userId}`);
  };

  return (
    <div className="payment-success">
      <h1>Payment Successful!</h1>
      <p>Your payment was processed successfully.</p>
      <button onClick={redirectToOrderPage}>View My Orders</button>
      {message && <p>{message}</p>}
    </div>
  );
}
