import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function ProductListPage({ products, setCart }) {
  const navigate = useNavigate();

  const handleBuy = (product) => {
    setCart((prevCart) => [...prevCart, product]);
    navigate('/cart');
  };

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
            <p><strong>Name:</strong> {prod.name}</p>
            <p><strong>Description:</strong> {prod.description}</p>
            <p><strong>Price:</strong> ${prod.price}</p>
            <p><strong>Gender:</strong> {prod.gender}</p>
            <p><strong>Size:</strong> {prod.size}</p>
            <p><strong>Brand:</strong> {prod.brand}</p>
            <p><strong>Sport:</strong> {prod.sport}</p>
            <p><strong>Quantity:</strong> {prod.quantity}</p>
            <p><strong>Condition:</strong> {prod.condition}</p>
            <p><strong>Manufacture Date:</strong> {prod.manufactureDate}</p>
            <p><strong>Average Rating:</strong> {prod.avgRating}</p>
            {prod.image && (
              <img
                src={URL.createObjectURL(prod.image)}
                alt={prod.name}
                style={{ width: '100px', height: '100px', objectFit: 'cover', marginTop: '10px' }}
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
                marginTop: '10px',
              }}
            >
              Buy
            </button>
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
