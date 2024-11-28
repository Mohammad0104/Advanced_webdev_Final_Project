import React, { useState, useEffect } from 'react';
import { checkLoginStatus, redirectTo, get_user_info } from './services/authService';
import { useNavigate, useLocation } from 'react-router-dom';
import { FRONTEND_BASE_URL, BACKEND_BASE_URL } from './constants';


function ProductPage({ products, setProducts }) {

  const navigate = useNavigate();
  const location = useLocation();

  const [product, setProduct] = useState({
    name: '',
    description: '',
    price: '', 
    gender: '',
    size: '',
    brand: '',
    sport: '',
    quantity: 1,
    condition: '',
    year_product_made: '',
    avgRating: '',
    image: null,
  });

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [seller_id, setSellerId] = useState(null);

  // Check login status as soon as the page is entered
  useEffect(() => {
    const checkStatus = async () => {
      const loginStatus = await checkLoginStatus(navigate);
      if (loginStatus) {
        setIsLoggedIn(true);
        const userInfo = await get_user_info();
        setSellerId(userInfo.id);

      } else {
        setIsLoggedIn(false);
        redirectTo(`/authorize?next=${FRONTEND_BASE_URL}${location.pathname}`);
      }
    };

    checkStatus();
  }, [navigate, location]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    const updatedValue = name === 'youth_size' ? value === 'true': value;

    setProduct((prev) => ({
      ...prev,
      [name]: updatedValue,
    }));
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
  
    // maximum size (in bytes)
    const MAX_FILE_SIZE = 16 * 1024 * 1024; // 16MBB

    if (file && file.size > MAX_FILE_SIZE) {
      alert('File size is too large. Please upload an image smaller than 2MB.');
      return; // Exit if file is too large
    }
    setProduct((prev) => ({
      ...prev,
      image: file, // Store the selected file
    }));
  };

//   const handleFormSubmit = async (event) => {
//     event.preventDefault(); // Prevent default form submission

//     const isLoggedIn = await checkLoginStatus(navigate);
//     if (isLoggedIn) {
//       const userInfo = await get_user_info();
//       console.log(userInfo);
//       product.seller_id = userInfo.id;
//       handleSubmit(event);
//     } else {
//         console.log('User not logged in. Form submission halted.');
//         redirectTo(`/authorize?next=${FRONTEND_BASE_URL}${location.pathname}`);
//     }
// };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const reader = new FileReader();
    reader.onload = async () => {
      const base64Image = reader.result; // Base64 string including metadata
      const payload = {
        seller_id: seller_id,
        name: product.name,
        description: product.description,
        price: product.price,
        gender: product.gender,
        size: product.size,
        youth_size: product.youth_size,
        featured: product.featured,
        brand: product.brand,
        sport: product.sport,
        quantity: product.quantity,
        condition: product.condition,
        year_product_made: product.year_product_made,
        avgRating: product.avgRating,
        image: base64Image, // send the Base64 image string here
      };

      try {
        const response = await fetch(`${BACKEND_BASE_URL}/create_product`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
      
        // Log the response status and the body
        // console.log('Response Status:', response.status);
        const responseBody = await response.text();
        // console.log('Response Body:', responseBody);

      
        if (!response.ok) {
          throw new Error(`Failed to create product: ${responseBody}`);
        }

        const result = JSON.parse(responseBody);  // Parse the response body as JSON
      
        // console.log('Product created successfully:', result);
        console.log('Product created successfully:', result);
        alert('Product added successfully!');
      } catch (error) {
        console.error('Error creating product:', error);
        alert('Failed to add the product');
      }
      
    };
    reader.readAsDataURL(product.image);
    
    // Reset form or update state
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
      year_product_made: '',
      avgRating: '',
      image: '',
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
          placeholder="Price ($)"
          value={product.price}
          onChange={handleChange}
          required
          onInput={(e) => {
            // allow backspace, delete, and valid input
            // (not allowing invalid characters or using more than 2 decimal places)
            const regex = /^(?:\d+(\.\d{0,2})?|\.\d{1,2})$/;
            const value = e.target.value;
        
            // if the input doesn't match the regex, reset the value to the last valid one
            if (!regex.test(value) && value !== '') {
              e.target.value = value.slice(0, -1);  // remove last character if invalid
            }
          }}
        />

        <select name="gender" value={product.gender} onChange={handleChange} required>
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Unisex">Unisex</option>
        </select>

        <select name="youth_size" value={product.youth_size} onChange={handleChange} required>
          <option value="">Select Age Group</option>
          <option value={true}>Youth</option>
          <option value={false}>Adult</option>
        </select>

        <select name="size" value={product.size} onChange={handleChange} required>
          <option value="">Select Size</option>
          <option value="Extra small">Extra small</option>
          <option value="Small">Small</option>
          <option value="Medium">Medium</option>
          <option value="Large">Large</option>
          <option value="Extra large">Extra large</option>
        </select>

        <select name="brand" value={product.brand} onChange={handleChange} required>
          <option value="">Select Brand</option>
          <option value="Adidas">Adidas</option>
          <option value="Asics">Asics</option>
          <option value="Bauer">Bauer</option>
          <option value="CCM">CCM</option>
          <option value="Diadora">Diadora</option>
          <option value="Louisville Slugger">Louisville Slugger</option>
          <option value="Marucci">Marucci</option>
          <option value="Mizuno">Mizuno</option>
          <option value="New Balance">New Balance</option>
          <option value="Nike">Nike</option>
          <option value="Oakley">Oakley</option>
          <option value="Puma">Puma</option>
          <option value="Rawlings">Rawlings</option>
          <option value="Reebok">Reebok</option>
          <option value="Sherwood">Sherwood</option>
          <option value="True">True</option>
          <option value="Umbro">Umbro</option>
          <option value="Under Armour">Under Armour</option>
          <option value="Venom">Venom</option>
          <option value="Warrior">Warrior</option>
          <option value="Wilson">Wilson</option>
        </select>

        <select name="sport" value={product.sport} onChange={handleChange} required>
          <option value="">Select Sport</option>
          <option value="Baseball">Baseball</option>
          <option value="Basketball">Basketball</option>
          <option value="Cricket">Cricket</option>
          <option value="Football">Football (American)</option>
          <option value="Rowing">Rowing</option>
          <option value="Soccer">Soccer</option>
          <option value="Tennis">Tennis</option>
          <option value="Volleyball">Volleyball</option>
          <option value="Other">Other</option>
        </select>

        <label>
          Quantity:
          <input
            type="number"
            name="quantity"
            value={product.quantity}
            onChange={handleChange}
            required
            min="1"
            step="1"
            onBlur={(e) => {
              // when the input loses focus, check if the value is below 1
              // (this way you can type values, but if you leave and it is invalid it changes to the default 1)
              if (parseInt(e.target.value) < 1) {
                e.target.value = 1;
              }
            }}
            style={{ display: 'block', marginTop: '5px' }}
          />
        </label>

        <select name="condition" value={product.condition} onChange={handleChange} required>
          <option value="">Select Condition</option>
          <option value="Brand New">Brand New</option>
          <option value="Slightly used">Slightly used</option>
          <option value="Used">Used</option>
          <option value="Heavily used">Heavily used</option>
        </select>

        <label>
          Manufacture Year:
          <select name="year_product_made" value={product.year_product_made} onChange={handleChange}>
            <option value="">Select Year</option>
            {Array.from({ length: 25 }, (_, i) => 2000 + i).map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </label>

        <label>
          Upload Image:
          <input type="file" onChange={handleImageChange} required />
        </label>

        <button type="submit">Add Product</button>
      </form>
    </div>
  );
}

export default ProductPage;
