// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';

// function ProfilePage() {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [isLogin, setIsLogin] = useState(true); // Toggle between login and register
//   const [name, setName] = useState(''); // New state for name
//   const [profilePicUrl, setProfilePicUrl] = useState(''); // New state for profile picture URL
  
//   // useEffect(() => {
//   //   const redirectToOAuth = async () => {
//   //     try {
//   //       const response = await fetch('/authorize');  // This will hit the backend route via the proxy
//   //       if (response.ok) {
//   //         window.location.href = response.url;  // Redirect user to OAuth login
//   //       }
//   //     } catch (error) {
//   //       console.error('Error redirecting to OAuth:', error);
//   //     }
//   //   };

//   //   redirectToOAuth();
//   // }, []);

//   useEffect(() => {
//     // Trigger OAuth redirection by calling the /authorize endpoint
//     const redirectToOAuth = async () => {
//       try {
//         const response = await fetch('/authorize'); // Request the OAuth URL from backend
//         if (response.ok) {
//           const oauthUrl = await response.text(); // Get the redirect URL from the response
//           window.location.href = oauthUrl; // Perform the actual redirect
//         } else {
//           console.error('Failed to fetch the OAuth URL.');
//         }
//       } catch (error) {
//         console.error('Error fetching OAuth URL:', error);
//       }
//     };

//     redirectToOAuth(); // Call the function to redirect user to OAuth
//   }, []);

//   // Placeholder function for registration
  

//   const handleRegister = () => {
//     alert(`Registration successful!\nName: ${name}\nEmail: ${email}\nProfile Picture URL: ${profilePicUrl}`);
//     // Additional logic can be added here to save user details
//   };

//   // Placeholder function for login
//   const handleLogin = () => {
//     alert(`Login successful!\nEmail: ${email}`);
//     // Additional logic for login can be added here
//   };

//   return (
//     <div className="profile-page">
//       <h1 className="profile-header">Your Profile</h1>
//       <form
//         onSubmit={(e) => {
//           e.preventDefault();
//           isLogin ? handleLogin() : handleRegister();
//         }}
//         className="profile-form"
//       >
//         {!isLogin && (
//           <>
//             <input
//               type="text"
//               placeholder="Name"
//               value={name}
//               onChange={(e) => setName(e.target.value)}
//               required
//               className="profile-input"
//             />
//             <input
//               type="text"
//               placeholder="Profile Picture URL"
//               value={profilePicUrl}
//               onChange={(e) => setProfilePicUrl(e.target.value)}
//               className="profile-input"
//             />
//           </>
//         )}
//         <input
//           type="email"
//           placeholder="Email"
//           value={email}
//           onChange={(e) => setEmail(e.target.value)}
//           required
//           className="profile-input"
//         />
//         <input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//           required
//           className="profile-input"
//         />
//         <button type="submit" className="profile-button">
//           {isLogin ? 'Login' : 'Register'}
//         </button>
//       </form>
//       <p className="toggle-text" onClick={() => setIsLogin(!isLogin)}>
//         {isLogin ? 'Create an account' : 'Already have an account? Login'}
//       </p>
//     </div>
//   );
// }

// export default ProfilePage;
import React from 'react';

const ProfilePage = () => {
  
  // This function redirects the user to the Flask OAuth authorize route
  const redirectToOAuth = () => {
    // Redirect to Flask backend for OAuth login
    window.location.href = 'http://localhost:8080/authorize';
  };

  return (
    <div>
      <h1>Profile Page</h1>
      
      {/* Button to initiate OAuth login */}
      <button onClick={redirectToOAuth}>
        Login with Google
      </button>

      {/* You can also display user data here if they are logged in */}
      <div id="user-info">
        {/* Add conditional rendering here for user information after OAuth flow is completed */}
      </div>
    </div>
  );
};

export default ProfilePage;
