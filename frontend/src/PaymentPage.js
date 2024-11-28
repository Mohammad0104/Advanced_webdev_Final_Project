import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import React, { useState, useEffect } from "react";

import CheckoutForm from "./CheckoutForm";
import "./PaymentPage.css";
import { BACKEND_BASE_URL } from "./constants";


export default function PaymentPage() {

    const [clientSecret, setClientSecret] = useState(null);
    const [loading, setLoading] = useState(true);
    // Parse publishable key here
    const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY);

    useEffect(() => {
        const loadData = async () => {
        try {
            const response = await fetch(`${BACKEND_BASE_URL}/create-payment-intent`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                items: [{ id: "Premium" }],
                customer: "user_uuid", 
            }),
            });

            const data = await response.json();

            if (data.clientSecret) {
            setClientSecret(data.clientSecret);
            } else {
            console.error('No client secret returned from server');
            }
        } catch (error) {
            console.error('Error fetching client secret:', error);
        } finally {
            setLoading(false); 
        }
        };

        loadData(); // Run the data loading function
    }, []); // Only run once when the component mounts

  // If still loading, show a loading message
  if (loading) {
    return <div>Loading...</div>;
  }


  if (!clientSecret) {
    console.error("client secret empty or undefined");
    return <div>Loading...</div>;  
  }

   const appearance = {
    theme: 'night',
  };
  const options = {
    clientSecret,
    appearance,
  };

  return (
    <Elements stripe={stripePromise} options={options}>
      <CheckoutForm />
    </Elements>
  );
};