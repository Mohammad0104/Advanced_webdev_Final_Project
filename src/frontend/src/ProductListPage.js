import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function ProductListPage({ setCart }) {
  const [products, setProducts] = useState([]); // Ensure initial state is an empty array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('/products'); // Make sure the URL is correct
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
  
        const data = await response.json();
        console.log('Fetched data:', data); // Log the entire data structure
  
        // Check if data.products is an array
        if (data && Array.isArray(data.products)) {
          setProducts(data.products); // Only set it if it's an array
        } else {
          console.error('Error: data.products is not an array:', data); // Log the actual data structure
          throw new Error('Expected an array of products');
        }
  
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
  
    fetchProducts();
  }, []); // Empty dependency array, so it runs only once when the component mounts
  

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
                src={`data:image/png;base64,${prod.image}`} // Assuming the backend sends base64-encoded data
                alt={prod.name}
                style={{ width: '500px', height: '400px', objectFit: 'cover', marginTop: '10px' }}
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
                marginTop: '20px', // Increase space between the image and button
                display: 'block', // Ensure the button is block-level and occupies the full width
                marginLeft: 'auto', // Center the button horizontally
                marginRight: 'auto',
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
