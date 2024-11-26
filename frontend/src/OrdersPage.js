import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { BACKEND_BASE_URL } from './constants';

export default function OrdersPage() {
  const { userId } = useParams();  // Get the userId from the URL
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch(`${BACKEND_BASE_URL}/orders/user/${userId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch orders');
        }
        const data = await response.json();
        setOrders(data.orders);  // Assuming the response has an "orders" array
        console.log(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchOrders();
  }, [userId]);

  if (loading) {
    return <p>Loading orders...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      <h1>Your Order History</h1>
      <div style={{borderRadius: '10px'}}>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id} style={{ marginBottom: '50px', border: "0.5px solid #696969", backgroundColor: '#E8E8E8', borderRadius: '10px' }}>
            <h3 style={{marginBottom: '0px', fontWeight: 'normal'}}><strong>Date:</strong> {order.order_date}</h3>
            <h3 style={{margin: '0px'}}>Total: ${order.total.toFixed(2)}</h3>
            <h4 style={{marginBottom: '0px', backgroundColor: '#C0C0C0'}}>Items:</h4>
            <div style={{ marginTop: '0px', marginBottom: '3px', backgroundColor: '#D3D3D3' }}>
              {order.items.map((item, index) => (
                <div key={index} style={{ marginBottom: '5px' }}>
                  {item.product_name} <br />
                  ${item.price.toFixed(2)} each <br />
                  <strong>Quantity:</strong> {item.quantity} <br />
                  <hr></hr >
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
    </div>
  );
}
