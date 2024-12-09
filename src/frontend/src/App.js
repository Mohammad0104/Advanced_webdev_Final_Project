// App.js
import './App.css';
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './HomePage'; // Import the HomePage component
import ProductPage from './ProductPage';
import ProductListPage from './ProductListPage';
import CartPage from './CartPage';
import ProfilePage from './ProfilePage';
import Review from './Review';

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Welcome to Our Marketplace</h1>
          <nav>
            <Link to="/" className="App-link">Home</Link>
            <Link to="/add-product" className="App-link">Add Product</Link>
            <Link to="/products" className="App-link">View Products</Link>
            <Link to="/cart" className="App-link">View Cart</Link>
            <Link to="/profile" className="App-link">Profile</Link>
            <Link to="/reviews" className="App-link">Reviews</Link>
          </nav>
        </header>
        <div className="App-content">
          <Routes>
            <Route path="/" element={<HomePage />} /> {/* Add HomePage route1 */}
            <Route path="/add-product" element={<ProductPage products={products} setProducts={setProducts} />} />
            <Route path="/products" element={<ProductListPage products={products} setCart={setCart} />} />
            <Route path="/cart" element={<CartPage cart={cart} />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/reviews" element={<Review />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
