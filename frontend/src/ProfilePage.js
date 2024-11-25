import React, { useState, useEffect } from 'react';
import { checkLoginStatus, redirectTo, get_user_info } from './services/authService';
import { redirect, useNavigate } from 'react-router-dom';

const ProfilePage = () => {
  const [user, setUser] = useState(null);  // User state to store logged-in user's info
  const [loading, setLoading] = useState(true);  // Loading state while checking login status

  const navigate = useNavigate();

  useEffect(() => {
    const initializePage = async () => {
      const isLoggedIn = await checkLoginStatus(navigate); // Use the checkLoginStatus function from authService
      if (isLoggedIn) {
        const userData = await get_user_info();
        setUser(userData);
      }
      setLoading(false); // Stop loading regardless of login status
    };

    initializePage(); // Run the initialization when the component mounts
  }, []); // Empty dependency array ensures this runs once on component mount
  

  // Redirect to Flask backend for OAuth login
  const redirectToOAuth = () => {
    redirectTo('/authorize');
    // window.location.href = 'http://localhost:8080/authorize';
  };

  // Handle log out
  const handleLogout = async () => {
    try {
      const response = await fetch('/logout', { method: 'POST' });  // API call to logout
      if (response.ok) {
        window.location.href = '/';  // Redirect to home or login page
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  // If the component is still loading, show a loading spinner or message
  if (loading) {
    return <div>Loading...</div>;
  }

  // If user is logged in, show their profile info
  if (user) {
    return (
      <div>
        <h1>Your Profile</h1>
        <div>
          <img src={user.profile_pic_url} alt="Profile" width="150" />
          <p>{user.name}</p>
          <p>{user.email}</p>
        </div>
        <button onClick={handleLogout}>Log Out</button>
      </div>
    );
  }

  // If the user is not logged in, show the login button
  return (
    <div>
      <h1>Profile Page</h1>
      <button onClick={redirectToOAuth}>Login with Google</button>
    </div>
  );
};

export default ProfilePage;
