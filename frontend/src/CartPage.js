import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FRONTEND_BASE_URL, BACKEND_BASE_URL } from './constants';
import { checkLoginStatus, get_user_info, redirectTo } from './services/authService';

function CartPage({ cart }) {
  // const [cart, setCart] = useState([]);
  const [localCart, setLocalCart] = useState(cart || []);
  const [showForm, setShowForm] = useState(false);
  const [userInfo, setUserInfo] = useState({
    name: '',
    address: '',
    deliveryDate: '',
  });

  const location = useLocation();
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  useEffect(() => {
    const checkStatus = async () => {
      const loginStatus = await checkLoginStatus(navigate);
      if (loginStatus) {
        setIsLoggedIn(true);
        const userInfo = await get_user_info();
        console.log(userInfo);
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
      const fetchCart = async () => {
        try {
          const response = await fetch(`${BACKEND_BASE_URL}/cart/${userData.id}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });
  
          if (response.ok) {
            const cartData = await response.json();
            console.log(cartData);
            setLocalCart(cartData.items); // Update the local state
            console.log(localCart);
            // cart = cartData.items || []; // Update cart state
          } else {
            console.error('Failed to fetch cart:', response.statusText);
          }
        } catch (error) {
          console.error('Error fetching cart:', error);
        }
      };
  
      fetchCart();
    }
  }, [userData]); // Only run getCart when userData is updated
  
  // Calculate the subtotal
  const subtotal = localCart.reduce((acc, item) => acc + parseFloat(item.product_price || 0) * item.quantity, 0);
  // const subtotal = cart.reduce((acc, item) => acc + parseFloat(item.price || 0), 0);

  const handleBuyNow = () => {
    if (localCart.length === 0) {
      alert("Your cart is empty. Add some products first!");
    } else {
      setShowForm(true); // Show the form when "Buy Now" is clicked
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prevInfo) => ({ ...prevInfo, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Order placed successfully!\nName: ${userInfo.name}\nAddress: ${userInfo.address}\nDelivery Date: ${userInfo.deliveryDate}\nSubtotal: $${subtotal.toFixed(2)}`);
    // You can add logic here to process the order and clear the cart
  };

  return (
    <div>
      <h1>Your Cart</h1>
      {localCart.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div>
          {localCart.map((item, index) => (
            <div
              key={index}
              style={{
                border: '1px solid #ddd',
                padding: '10px',
                marginBottom: '10px',
                borderRadius: '5px',
              }}
            >
              <p><strong>{item.product_name}</strong></p>
              <p>${(item.product_price ?? 0).toFixed(2)} each</p>
              <p><strong>Quantity:</strong> {item.quantity}</p>
            </div>
          ))}
          <p>
            <strong>Subtotal:</strong> ${subtotal.toFixed(2)}
          </p>
          <button
            onClick={handleBuyNow}
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '20px',
            }}
          >
            Proceed to Checkout
          </button>

          {showForm && (
            <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
              <h2>Enter Your Information</h2>
              <input
                type="text"
                name="name"
                placeholder="Name"
                value={userInfo.name}
                onChange={handleInputChange}
                required
                style={{ display: 'block', marginBottom: '10px', padding: '8px', width: '100%' }}
              />
              <input
                type="text"
                name="address"
                placeholder="Address"
                value={userInfo.address}
                onChange={handleInputChange}
                required
                style={{ display: 'block', marginBottom: '10px', padding: '8px', width: '100%' }}
              />
              <input
                type="date"
                name="deliveryDate"
                value={userInfo.deliveryDate}
                onChange={handleInputChange}
                required
                style={{ display: 'block', marginBottom: '10px', padding: '8px', width: '100%' }}
              />
              <button
                type="submit"
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#0066cc',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                }}
              >
                Submit
              </button>
            </form>
          )}
        </div>
      )}
    </div>
  );
}

export default CartPage;
