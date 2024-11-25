import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

function ProductDetailPage() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await fetch(`http://localhost:8080/product/${productId}`);
        if (!response.ok) {
          throw new Error("Product not found");
        }
        const data = await response.json();
        setProduct(data.product);
        setFormData(data.product);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
      setFormData((prevFormData) => ({
        ...prevFormData,
        image: reader.result, // Base64 encode the image
      }));
    };
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async () => {
    try {
      const response = await fetch(`http://localhost:8080/product/${productId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update product");
      }

      const data = await response.json();
      setProduct(data.product); // Update the state with the updated product
      setIsEditing(false); // Exit edit mode
      alert("Product updated successfully!");
    } catch (err) {
      console.error("Error updating product:", err);
      alert(`Error: ${err.message}`);
    }
  };

  if (loading) {
    return <p style={{ textAlign: "center", marginTop: "20px" }}>Loading product details...</p>;
  }

  if (error) {
    return <p style={{ textAlign: "center", color: "red", marginTop: "20px" }}>{error}</p>;
  }

  if (isEditing) {
    return (
      <div
        style={{
          maxWidth: "800px",
          margin: "20px auto",
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "10px",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "20px" }}>Edit Product</h2>
        <form style={{ display: "grid", gap: "15px" }}>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name || ""}
              onChange={handleInputChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
              }}
            />
          </label>
          <label>
            Description:
            <textarea
              name="description"
              value={formData.description || ""}
              onChange={handleInputChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
              }}
            />
          </label>
          <label>
            Price:
            <input
              type="number"
              name="price"
              value={formData.price || ""}
              onChange={handleInputChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
              }}
            />
          </label>
          <label>
            Gender:
            <select
              name="gender"
              value={formData.gender || ""}
              onChange={handleInputChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
              }}
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Unisex">Unisex</option>
            </select>
          </label>
          <label>
            Size:
            <select
              name="size"
              value={formData.size || ""}
              onChange={handleInputChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
              }}
            >
              <option value="">Select Size</option>
              <option value="Extra Small">Extra Small</option>
              <option value="Small">Small</option>
              <option value="Medium">Medium</option>
              <option value="Large">Large</option>
              <option value="Extra Large">Extra Large</option>
            </select>
          </label>
          <label>
            Condition:
            <select
              name="condition"
              value={formData.condition || ""}
              onChange={handleInputChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "5px",
                border: "1px solid #ccc",
              }}
            >
              <option value="">Select Condition</option>
              <option value="New">New</option>
              <option value="Slightly Used">Slightly Used</option>
              <option value="Moderately Used">Moderately Used</option>
              <option value="Heavily Used">Heavily Used</option>
            </select>
          </label>
          <label>
            Image:
            <input type="file" onChange={handleImageChange} style={{ marginTop: "5px" }} />
          </label>
        </form>
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: "20px" }}>
          <button
            onClick={handleSave}
            style={{
              padding: "10px 15px",
              backgroundColor: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              width: "48%",
            }}
          >
            Save
          </button>
          <button
            onClick={() => setIsEditing(false)}
            style={{
              padding: "10px 15px",
              backgroundColor: "#6c757d",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              width: "48%",
            }}
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "20px auto",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "10px",
        backgroundColor: "#f9f9f9",
      }}
    >
      <h2 style={{ textAlign: "center", fontSize: "24px", color: "#333", marginBottom: "20px" }}>Product Details</h2>
      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <p style={{ fontSize: "20px", margin: "5px 0" }}>
          <strong>Name:</strong> {product.name}
        </p>
        <p style={{ fontSize: "20px", margin: "5px 0" }}>
          <strong>Price:</strong> ${product.price}
        </p>
      </div>
      <div style={{ margin: "20px 0", textAlign: "center" }}>
        {product.image && <img src={`data:image/png;base64,${product.image}`} alt={product.name} style={{ maxWidth: "100%", height: "auto", borderRadius: "10px" }} />}
      </div>
      <p>
        <strong>Description:</strong> {product.description}
      </p>
      <p>
        <strong>Brand:</strong> {product.brand}
      </p>
      <p>
        <strong>Sport:</strong> {product.sport}
      </p>
      <p>
        <strong>Condition:</strong> {product.condition}
      </p>
      <p>
        <strong>Gender:</strong> {product.gender}
      </p>
      <p>
        <strong>Size:</strong> {product.size}
      </p>
      <p>
        <strong>Quantity:</strong> {product.quantity}
      </p>
      <p>
        <strong>Manufacture Date:</strong> {product.year_product_made || "Unknown"}
      </p>
      <div style={{ textAlign: "center", marginTop: "20px", display: 'flex', justifyContent: 'center' }}>
        <button
          onClick={() => setIsEditing(true)}
          style={{
            padding: "10px 15px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Edit Product
        </button>
      </div>
      <div style={{ textAlign: "center", marginTop: "20px", display: 'flex', justifyContent: 'center'}}>
        <button
          onClick={() => navigate(`/reviews/product/${productId}`, { state: { productId } })} // Navigate to review page
          // onClick={() => navigate(`/product/${productId}/review`)} // Navigate to review page
          style={{
            padding: "10px 15px",
            backgroundColor: "#28a745",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
            marginLeft: "10px", // Optional spacing if placed next to Edit button
          }}
        >
          Reviews
        </button>
</div>

    </div>
  );
}

export default ProductDetailPage;
