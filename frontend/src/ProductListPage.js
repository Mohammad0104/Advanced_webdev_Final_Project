import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { BACKEND_BASE_URL } from './constants';

function ProductListPage({ setCart }) {
  const [products, setProducts] = useState([]); // Initial state as an empty array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
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

    fetchProducts();
  }, []); // Run once when the component mounts

  const handleBuy = (product) => {
    setCart((prevCart) => [...prevCart, product]);
    navigate('/cart');
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
            }}
          >
            <p>
              <strong>Name:</strong> {prod.name}
            </p>
            <p>
              <strong>Price:</strong> ${prod.price}
            </p>
            <p>
              <strong>Description:</strong> {prod.description || 'No description available'}
            </p>
            <p>
              <strong>Gender:</strong> {prod.gender}
            </p>
            <p>
              <strong>Size:</strong> {prod.size}
            </p>
            <p>
              <strong>Brand:</strong> {prod.brand}
            </p>
            <p>
              <strong>Sport:</strong> {prod.sport}
            </p>
            <p>
              <strong>Condition:</strong> {prod.condition}
            </p>
            <p>
              <strong>Average Rating:</strong> {prod.avgRating || 'N/A'}
            </p>
            {prod.image && (
              <img
                src={prod.image.startsWith('data:') ? prod.image : `data:image/png;base64,${prod.image}`}
                alt={prod.name}
                style={{
                  width: '100%',
                  maxHeight: '400px',
                  objectFit: 'cover',
                  marginTop: '10px',
                  borderRadius: '5px',
                }}
              />
            )}
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
              Buy
            </button>
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
