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
        const response = await fetch(`/product/${productId}`);
        if (!response.ok) {
          throw new Error('Product not found');
        }
        const data = await response.json();
        setProduct(data.product);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  if (loading) {
    return <p>Loading product details...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  let age_group;
  if (product.youth_size == true) {
    age_group = 'Youth';
  }
  else {
    age_group = 'Adult';
  }

  return (
    <div style={{ maxWidth: '800px', margin: '20px auto', padding: '20px' }}>
      <h1>{product.name}</h1>
      <h2>${product.price}</h2>
      <p><strong>Description:</strong> {product.description}</p>
      <p>{product.brand}&emsp;{product.sport}</p>
      <p>{product.condition}</p>
      <p>{age_group} {product.gender}&emsp;{product.size}</p>
      <p><strong>Listed at: </strong>{product.date_listed}</p>
      <p><strong>Quantity:</strong> {product.quantity}</p>
      <p><strong>Manufacture Date:</strong> {product.manufactureDate || "unknown"}</p>
      {product.image && (
        <img
          src={`data:image/png;base64,${product.image}`} // Assuming base64 image data
          alt={product.name}
          style={{ width: '500px', height: '400px', objectFit: 'cover', marginTop: '10px' }}
        />
      )}
      
      {/* Flexbox container for the two buttons */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
        <button
          onClick={() => navigate('/')} // Navigate to home
          style={{
            padding: '10px 15px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            width: '48%' // Make the buttons take up 48% of the width each
          }}
        >
          Back to Home
        </button>

        <button
          onClick={() => navigate('/products')} // Navigate to product list
          style={{
            padding: '10px 15px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            width: '48%' // Make the buttons take up 48% of the width each
          }}
        >
          Back to Product List
        </button>
      </div>
    </div>
  );
}

export default ProductDetailPage;
