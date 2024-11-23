import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function ProductDetailPage() {
  const { productId } = useParams(); // Get the product ID from the URL
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://localhost:8080/products/${productId}`);
        if (!response.ok) {
          throw new Error('Product not found');
        }
        const data = await response.json();
        setProduct(data.product);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  if (loading) return <p>Loading product details...</p>;

  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  // Determine the age group
  const ageGroup = product.youth_size ? 'Youth' : 'Adult';

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>{product.name}</h1>
      <h2 style={{ color: '#007bff' }}>${product.price}</h2>
      <p><strong>Description:</strong> {product.description || 'No description provided.'}</p>
      <p><strong>Brand:</strong> {product.brand}</p>
      <p><strong>Sport:</strong> {product.sport}</p>
      <p><strong>Condition:</strong> {product.condition}</p>
      <p><strong>Age Group:</strong> {ageGroup}</p>
      <p><strong>Gender:</strong> {product.gender}</p>
      <p><strong>Size:</strong> {product.size}</p>
      <p><strong>Listed at:</strong> {product.date_listed || 'Unknown'}</p>
      <p><strong>Quantity:</strong> {product.quantity}</p>
      <p><strong>Manufacture Date:</strong> {product.manufactureDate || 'Unknown'}</p>

      {product.image && (
        <img
          src={`data:image/png;base64,${product.image}`} // Assuming base64 image data
          alt={product.name}
          style={{
            width: '100%',
            maxWidth: '500px',
            height: 'auto',
            objectFit: 'cover',
            marginTop: '10px',
            borderRadius: '10px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          }}
        />
      )}

      {/* Flexbox container for buttons */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
        <button
          onClick={() => navigate('/')} // Navigate to home
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#0056b3')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#007bff')}
        >
          Back to Home
        </button>

        <button
          onClick={() => navigate('/products')} // Navigate to product list
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#0056b3')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#007bff')}
        >
          Back to Product List
        </button>
      </div>
    </div>
  );
}

export default ProductDetailPage;
