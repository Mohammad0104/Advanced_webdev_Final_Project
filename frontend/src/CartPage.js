import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FRONTEND_BASE_URL, BACKEND_BASE_URL } from './constants';
import { checkLoginStatus, get_user_info, redirectTo } from './services/authService';

function CartPage({ cart }) {
  const [localCart, setLocalCart] = useState(cart || []);
  const [cartId, setCardId] = useState(null);
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
            setLocalCart(cartData.items);
            setCardId(cartData.id)
          } else {
            console.error('Failed to fetch cart:', response.statusText);
          }
        } catch (error) {
          console.error('Error fetching cart:', error);
        }
      };

      fetchCart();
    }
  }, [userData]);

  let subtotal = 0;
  if (localCart) {
    subtotal = localCart.reduce((acc, item) => acc + parseFloat(item.product_price || 0) * item.quantity, 0);
  }

  // Function to update quantity
  const updateQuantityInDB = async (itemId, newQuantity) => {
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/cart/${cartId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_id: itemId,
          quantity: newQuantity,
          subtotal: subtotal
        }),
      });
      if (response.ok) {
        const updatedCart = await response.json();
        console.log(updatedCart);
        setLocalCart(updatedCart.items);
      } else {
        console.error('Failed to update quantity:', response.statusText);
        alert("Cannot increase quantity since there isn't enough of the product, to add more to cart");
      }
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  const handleQuantityChange = (itemId, change) => {
    const item = localCart.find(item => item.product_id === itemId);
    const newQuantity = Math.max(item.quantity + change, 1); // Ensure quantity is at least 1
    updateQuantityInDB(itemId, newQuantity);
  };

  // Function to remove item from cart
  const removeItemFromDB = async (itemId) => {
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/cart/${cartId}/remove`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cart_item_id: itemId,
        }),
      });
      if (response.ok) {
        const updatedCart = await response.json();
        console.log(updatedCart);
        setLocalCart(updatedCart.items);
        alert('Product(s) removed from cart successfully');
      } else {
        console.error('Failed to remove item:', response.statusText);
      }
    } catch (error) {
      console.error('Error removing item:', error);
    }
  };

  const handleRemoveItem = (itemId) => {
    removeItemFromDB(itemId);
  };

  const handleBuyNow = () => {
    if (localCart.length === 0) {
      alert("Your cart is empty. Add some products first!");
    } else {
      navigate('/paymentpage');
      // setShowForm(true);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prevInfo) => ({ ...prevInfo, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Order placed successfully!\nName: ${userInfo.name}\nAddress: ${userInfo.address}\nDelivery Date: ${userInfo.deliveryDate}\nSubtotal: $${subtotal.toFixed(2)}`);
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
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                width: '100%',
                maxWidth: '877px'
              }}
            >
              <div style={{ marginLeft: '11%', width: '80%'}}>
                <p><strong>{item.product_name}</strong></p>
                <p>${(item.product_price ?? 0).toFixed(2)} each</p>
                <p><strong>Quantity:</strong> 
                  <button 
                    onClick={() => handleQuantityChange(item.product_id, -1)} 
                    style={{ margin: '0 10px', padding: '8px', cursor: 'pointer', fontWeight: 'bold' }}
                    disabled={item.quantity <= 1}
                  >
                    -
                  </button>
                  {item.quantity}
                  <button 
                    onClick={() => handleQuantityChange(item.product_id, 1)} 
                    style={{ margin: '0 10px', padding: '8px', cursor: 'pointer', fontWeight: 'bold' }}
                  >
                    +
                  </button>
                </p>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', marginLeft: '10px', marginRight: '5%' }}>
                <button 
                  onClick={() => handleRemoveItem(item.product_id)} 
                  style={{ background: 'red', color: 'white', padding: '10px 15px 10px 15px', borderRadius: '50%', cursor: 'pointer', fontSize: 'x-large' }}
                >
                  X
                </button>
              </div>
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
// import React, { useState, useEffect } from 'react';
// import { useNavigate, useLocation } from 'react-router-dom';
// import { FRONTEND_BASE_URL, BACKEND_BASE_URL } from './constants';
// import { checkLoginStatus, get_user_info, redirectTo } from './services/authService';

// function CartPage({ cart }) {
//   const [localCart, setLocalCart] = useState(cart || []);
//   const [cartId, setCardId] = useState(null);
//   const [showForm, setShowForm] = useState(false);
//   const [userInfo, setUserInfo] = useState({
//     name: '',
//     address: '',
//     deliveryDate: '',
//   });
//   const [errorMessage, setErrorMessage] = useState('');
//   const location = useLocation();
//   const navigate = useNavigate();
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [userData, setUserData] = useState(null);

//   useEffect(() => {
//     const checkStatus = async () => {
//       const loginStatus = await checkLoginStatus(navigate);
//       if (loginStatus) {
//         setIsLoggedIn(true);
//         const userInfo = await get_user_info();
//         setUserData(userInfo);
//       } else {
//         setIsLoggedIn(false);
//         redirectTo(`/authorize?next=${FRONTEND_BASE_URL}${location.pathname}`);
//       }
//     };

//     checkStatus();
//   }, [navigate, location.pathname]);

//   useEffect(() => {
//     if (userData) {
//       const fetchCart = async () => {
//         try {
//           const response = await fetch(`${BACKEND_BASE_URL}/cart/${userData.id}`, {
//             method: 'GET',
//             headers: {
//               'Content-Type': 'application/json',
//             },
//           });

//           if (response.ok) {
//             const cartData = await response.json();
//             setLocalCart(cartData.items);
//             setCardId(cartData.id);
//           } else {
//             console.error('Failed to fetch cart:', response.statusText);
//           }
//         } catch (error) {
//           console.error('Error fetching cart:', error);
//         }
//       };

//       fetchCart();
//     }
//   }, [userData]);

//   let subtotal = 0;
//   if (localCart) {
//     subtotal = localCart.reduce((acc, item) => acc + parseFloat(item.product_price || 0) * item.quantity, 0);
//   }

//   const updateQuantityInDB = async (itemId, newQuantity) => {
//     try {
//       const response = await fetch(`${BACKEND_BASE_URL}/cart/update/${cartId}`, {
//         method: 'PUT',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           product_id: itemId,
//           quantity: newQuantity,
//           subtotal: subtotal,
//         }),
//       });
//       if (response.ok) {
//         const updatedCart = await response.json();
//         setLocalCart(updatedCart.items);
//       } else {
//         const errorData = await response.json();
//         if (errorData && errorData.message) {
//           alert(errorData.message); // Notify user of any server-defined error
//         } else {
//           console.error('Failed to update quantity:', response.statusText);
//         }
//       }
//     } catch (error) {
//       console.error('Error updating quantity:', error);
//     }
//   };
  

//   const handleQuantityChange = (itemId, change) => {
//     const item = localCart.find((item) => item.product_id === itemId);
//     const newQuantity = Math.max(item.quantity + change, 1); // Ensure quantity is at least 1
//     updateQuantityInDB(itemId, newQuantity);
//   };

//   return (
//     <div>
//       <h1>Your Cart</h1>
//       {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
//       {localCart.length === 0 ? (
//         <p>Your cart is empty.</p>
//       ) : (
//         <div>
//           {localCart.map((item, index) => (
//             <div key={index} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px', borderRadius: '5px' }}>
//               <p>
//                 <strong>{item.product_name}</strong>
//               </p>
//               <p>${(item.product_price ?? 0).toFixed(2)} each</p>
//               <p>
//                 <strong>Quantity:</strong>
//                 <button
//                   onClick={() => handleQuantityChange(item.product_id, -1)}
//                   disabled={item.quantity <= 1}
//                   style={{ margin: '0 10px', padding: '5px' }}
//                 >
//                   -
//                 </button>
//                 {item.quantity}
//                 <button
//                   onClick={() => handleQuantityChange(item.product_id, 1)}
//                   disabled={item.quantity >= item.available_stock}
//                   style={{ margin: '0 10px', padding: '5px' }}
//                 >
//                   +
//                 </button>
//               </p>
//             </div>
//           ))}
//           <p>
//             <strong>Subtotal:</strong> ${subtotal.toFixed(2)}
//           </p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default CartPage;
