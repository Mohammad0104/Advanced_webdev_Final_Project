import React, { useState } from 'react';

function ProfilePage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and register
  const [name, setName] = useState(''); // New state for name
  const [profilePicUrl, setProfilePicUrl] = useState(''); // New state for profile picture URL

  // Placeholder function for registration
  const handleRegister = () => {
    alert(`Registration successful!\nName: ${name}\nEmail: ${email}\nProfile Picture URL: ${profilePicUrl}`);
    // Additional logic can be added here to save user details
  };

  // Placeholder function for login
  const handleLogin = () => {
    alert(`Login successful!\nEmail: ${email}`);
    // Additional logic for login can be added here
  };

  return (
    <div className="profile-page">
      <h1 className="profile-header">Your Profile</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          isLogin ? handleLogin() : handleRegister();
        }}
        className="profile-form"
      >
        {!isLogin && (
          <>
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="profile-input"
            />
            <input
              type="text"
              placeholder="Profile Picture URL"
              value={profilePicUrl}
              onChange={(e) => setProfilePicUrl(e.target.value)}
              className="profile-input"
            />
          </>
        )}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="profile-input"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="profile-input"
        />
        <button type="submit" className="profile-button">
          {isLogin ? 'Login' : 'Register'}
        </button>
      </form>
      <p className="toggle-text" onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? 'Create an account' : 'Already have an account? Login'}
      </p>
    </div>
  );
}

export default ProfilePage;
