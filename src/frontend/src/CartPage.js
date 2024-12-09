import React, { useState } from 'react';

function CartPage({ cart }) {
  const [showForm, setShowForm] = useState(false);
  const [userInfo, setUserInfo] = useState({
    name: '',
    address: '',
    deliveryDate: '',
  });

  // Calculate the subtotal
  const subtotal = cart.reduce((acc, item) => acc + parseFloat(item.price || 0), 0);

  const handleBuyNow = () => {
    if (cart.length === 0) {
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
      {cart.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div>
          {cart.map((item, index) => (
            <div
              key={index}
              style={{
                border: '1px solid #ddd',
                padding: '10px',
                marginBottom: '10px',
                borderRadius: '5px',
              }}
            >
              <p><strong>Name:</strong> {item.name}</p>
              <p><strong>Condition:</strong> {item.condition}</p>
              <p><strong>Price:</strong> {item.price}</p>
            </div>
          ))}
          <p><strong>Subtotal:</strong> ${subtotal.toFixed(2)}</p>
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
            Buy Now
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
