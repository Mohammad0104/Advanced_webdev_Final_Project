import React, { useState } from 'react';

function ProductPage({ products, setProducts }) {
  const [product, setProduct] = useState({
    name: '',
    description: '',
    price: '', // Manually input price as text
    gender: '',
    size: '',
    brand: '',
    sport: '',
    quantity: 1,
    condition: '',
    manufactureDate: '',
    avgRating: '',
    image: null,
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setProduct((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleImageChange = (event) => {
    setProduct((prev) => ({
      ...prev,
      image: event.target.files[0], // Store the selected file
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setProducts([...products, { ...product, id: products.length + 1 }]);
    setProduct({
      name: '',
      description: '',
      price: '',
      gender: '',
      size: '',
      brand: '',
      sport: '',
      quantity: 1,
      condition: '',
      manufactureDate: '',
      avgRating: '',
      image: null,
    });
  };

  return (
    <div>
      <h1>Product Page</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input type="text" name="name" placeholder="Name" value={product.name} onChange={handleChange} required />
        <input type="text" name="description" placeholder="Description" value={product.description} onChange={handleChange} required />
        <input
          type="text"
          name="price"
          placeholder="Price (e.g., $10)"
          value={product.price}
          onChange={handleChange}
          required
        />

        <select name="gender" value={product.gender} onChange={handleChange} required>
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>

        <select name="size" value={product.size} onChange={handleChange} required>
          <option value="">Select Size</option>
          <option value="Large">Large</option>
          <option value="Medium">Medium</option>
          <option value="Small">Small</option>
        </select>

        <select name="brand" value={product.brand} onChange={handleChange} required>
          <option value="">Select Brand</option>
          <option value="Adidas">Adidas</option>
          <option value="Nike">Nike</option>
          <option value="Puma">Puma</option>
        </select>

        <select name="sport" value={product.sport} onChange={handleChange} required>
          <option value="">Select Sport</option>
          <option value="Soccer">Soccer</option>
          <option value="Basketball">Basketball</option>
          <option value="Tennis">Tennis</option>
          <option value="Baseball">Baseball</option>
          <option value="Cricket">Cricket</option>
        </select>

        <label>
          Quantity:
          <input
            type="number"
            name="quantity"
            value={product.quantity}
            onChange={handleChange}
            required
            style={{ display: 'block', marginTop: '5px' }}
          />
        </label>

        <select name="condition" value={product.condition} onChange={handleChange} required>
          <option value="">Select Condition</option>
          <option value="New">New</option>
          <option value="Old">Old</option>
        </select>

        <label>
          Manufacture Date:
          <input type="date" name="manufactureDate" value={product.manufactureDate} onChange={handleChange} required />
        </label>

        <label>
          Upload Image:
          <input type="file" onChange={handleImageChange} required />
        </label>

        <input
          type="number"
          step="0.1"
          name="avgRating"
          placeholder="Average Rating"
          value={product.avgRating}
          onChange={handleChange}
        />

        <button type="submit">Add Product</button>
      </form>
    </div>
  );
}

export default ProductPage;
