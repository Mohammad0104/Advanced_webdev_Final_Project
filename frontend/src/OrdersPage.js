import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

export default function OrdersPage() {
  const { userId } = useParams();  // Get the userId from the URL
  const [orders, setOrders] = useState([]);

  // Example fetch function to get orders
  useEffect(() => {

  }, [userId]);

  return (
    <div>
      <h1>Orders for User {userId}</h1>
      <ul>
        {orders.length === 0 ? (
          <p>No orders found.</p>
        ) : (
          orders.map((order) => (
            <li key={order.id}>
              Order ID: {order.id} - Status: {order.status}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
