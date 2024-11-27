import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FRONTEND_BASE_URL } from './constants';
import { checkLoginStatus, redirectTo, get_user_info } from './services/authService';

export default function PaymentSuccessPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [userData, setUserData] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [message, setMessage] = useState('');

  useEffect(() => {
    const checkStatus = async () => {
      const loginStatus = await checkLoginStatus(navigate);
      if (loginStatus) {
        setIsLoggedIn(true);
        const userInfo = await get_user_info();
        setUserData(userInfo);
      } else {
        setIsLoggedIn(false);
        redirectTo(`/authorize?next=${FRONTEND_BASE_URL}${location.pathname}`);
      }
    };

    checkStatus();
  }, [navigate, location.pathname]);


  useEffect(() => {
    if (userData) {
      const createOrder = async () => {
        try {
          const response = await fetch(`${FRONTEND_BASE_URL}/orders/create/${userData.id}`, {
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
      }
      createOrder();
    };
  }, [navigate, userData]); // Dependencies to ensure it runs only when `navigate` or `userId` changes

  // Function to navigate to the order page
  const redirectToOrderPage = () => {
    if (userData) {
      navigate(`/orders/${userData.id}`);
    }
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
