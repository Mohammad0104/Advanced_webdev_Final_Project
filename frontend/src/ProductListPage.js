import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { BACKEND_BASE_URL, FRONTEND_BASE_URL } from './constants';
import { checkLoginStatus, get_user_info, redirectTo } from './services/authService';

function ProductListPage({ setCart }) {
  const [products, setProducts] = useState([]); // Initial state as an empty array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const navigate = useNavigate();
  const location = useLocation();

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

    const fetchProducts = async () => {
      try {
        const response = await fetch(`${BACKEND_BASE_URL}/products`);
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }

        const data = await response.json();
        console.log('Fetched data:', data); // Debugging the fetched data

        if (data && Array.isArray(data.products)) {
          setProducts(data.products);
        } else {
          throw new Error('Expected an array of products in the response');
        }

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    checkStatus();
    fetchProducts();
  }, []); // Run once when the component mounts

  const handleBuy = async (product) => {
    console.log(product);

    const payload = {
      product_id: product.id,
      quantity: 1
    }

    if (product.quantity >= 1) {
      try {
          const response = await fetch(`${BACKEND_BASE_URL}/cart/${userData.id}/add`, {
              method: 'POST',
              body: JSON.stringify(payload),
              headers: {
                'Content-Type': 'application/json'
              }
          });

          const data = await response.json();
          console.log("Cart updated:", data);

          // Assuming the cart needs to be updated in the state
          setCart((prevCart) => [...prevCart, product]);

          // Navigate to the cart page
          alert(`1 ${product.name} added to cart`)
          // navigate('/cart');
      } catch (error) {
          console.error("Error updating cart:", error);
      }
    }
    else {
      alert('Cannot add to cart because the item is currently sold out');
    }
};




  if (loading) {
    return <p style={{ textAlign: 'center' }}>Loading products...</p>;
  }

  if (error) {
    return <p style={{ textAlign: 'center', color: 'red' }}>{error}</p>;
  }

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Listed Products</h1>
      {products.length === 0 ? (
        <p style={{ textAlign: 'center' }}>No products added yet.</p>
      ) : (
        products.map((prod) => (
          <div
            key={prod.id}
            style={{
              border: '1px solid #ddd',
              padding: '15px',
              marginBottom: '15px',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
              backgroundColor: prod.featured ? '#fffacd' : 'white', // Light gold for featured, white otherwise
            }}
          >
            <p>
              <strong>{prod.name}</strong>
            </p>
            <p style={{fontStyle: 'italic', fontWeight: 'bold'}}>
              ${prod.price.toFixed(2)}
            </p>
            <p>
              {prod.youth_size ? 'Youth' : 'Adult'} {prod.gender} {prod.size}
            </p>
            <p>
              {prod.condition}
            </p>
            {prod.image && (
              <img
                src={prod.image.startsWith('data:') ? prod.image : `data:image/png;base64,${prod.image}`}
                alt={prod.name}
                style={{
                  width: '90%',
                  maxHeight: '250px',
                  objectFit: 'scale-down',
                  marginTop: '10px',
                  borderRadius: '5px',
                }}
              />
            )}
            {prod.quantity === 0 ? (
            <p
              style={{
                color: 'red',
                fontWeight: 'bold',
                textAlign: 'center',
                marginTop: '10px',
              }}
            >
              SOLD OUT
            </p> ) : (
              <button
                onClick={() => handleBuy(prod)}
                style={{
                  padding: '10px 15px',
                  backgroundColor: '#007bff',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  marginTop: '20px',
                  display: 'block',
                  marginLeft: 'auto',
                  marginRight: 'auto',
                }}
              >
                Add to Cart
              </button>
            )}
            <Link
              to={`/product/${prod.id}`}
              style={{
                display: 'block',
                textAlign: 'center',
                textDecoration: 'none',
                color: '#007bff',
                marginTop: '10px',
              }}
            >
              View Details
            </Link>
          </div>
        ))
      )}
      <Link
        to="/"
        style={{
          display: 'block',
          marginTop: '20px',
          textAlign: 'center',
          textDecoration: 'none',
          color: '#007bff',
        }}
      >
        Back to Product Page
      </Link>
    </div>
  );
}

export default ProductListPage;
