import React, { useState } from 'react';  // Ensure useState is imported
import { useNavigate } from 'react-router-dom';  // Replace useHistory with useNavigate
import { useStripe, useElements, PaymentElement, LinkAuthenticationElement } from '@stripe/react-stripe-js';
import { FRONTEND_BASE_URL } from './constants';

export default function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();
  const navigate = useNavigate();  // Use useNavigate instead of useHistory

  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [paymentMethod, setPaymentMethod] = useState(null);

  const paymentElementOptions = {
    layout: 'accordion',
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!stripe || !elements) {
      return;
    }

    setIsLoading(true);

    const paymentElement = elements.getElement(PaymentElement);
    if (!paymentElement) {
      console.error("PaymentElement not found");
      setIsLoading(false);
      return;
    }

    // Confirm Payment
    const { error, paymentIntent } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${FRONTEND_BASE_URL}/payment-success`,  // Your return URL
      },
    });


    if (error) {
      setMessage(error.message);  // Display error message
      setIsLoading(false);
    } else if (paymentIntent && paymentIntent.status === 'succeeded') {
      setMessage('Payment succeeded!');
      setIsLoading(false);
      // Redirect to a success page (could be a confirmation page or a new route)
      navigate('/');  // Use navigate() to redirect
    } else {
      setMessage('Payment failed. Please try again.');
      setIsLoading(false);
    }
  };

  const handleEmailChange = (e) => {
    if (e.target && e.target.value) {
      setEmail(e.target.value);
    }
  };

  return (
    <form id="payment-form" onSubmit={handleSubmit}>
      <LinkAuthenticationElement
        id="link-authentication-element"
        onChange={handleEmailChange}
      />
      <PaymentElement id="payment-element" options={paymentElementOptions} />
      <button disabled={isLoading || !stripe || !elements} id="submit">
        <span id="button-text">
          {isLoading ? <div className="spinner" id="spinner"></div> : "Pay now"}
        </span>
      </button>
      {message && <div id="payment-message">{message}</div>}
    </form>
  );
}
