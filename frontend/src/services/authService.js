// Utility function that checks login status and handles navigation
export async function checkLoginStatus(navigate) {
    try {
        const response = await fetch('/check_login_status', {
            method: 'GET',
            credentials: 'include', // Ensures cookies are sent with the request
        });
        const data = await response.json();

        if (!data.logged_in) {
            console.warn('User not logged in');
            //window.location.href = 'http://localhost:8080/authorize';
            return false;
        }

        console.log('User is logged in.');
        return true;
    } catch (error) {
        console.error('Error checking login status:', error);
        navigate('/profile'); // Optional: Redirect to an error page
        return false;
    }
}


export async function redirectTo(route) {
    console.log('Redirecting...');
    window.location.href = 'http://localhost:8080'+route;
}


export async function get_oauth_user_info(){
    try {
        const response = await fetch('/user_info'); // Fetch user info from backend
        if (response.ok) {
          const oauthUserInfo = await response.json();
          return oauthUserInfo;
        //   setUser(userData); // Set user data if logged in
        } else {
            return null;
        //   setUser(null); // Set user to null if backend response is not ok
        }
      } catch (error) {
        console.error('Error fetching oauth user info:', error);
        return null;
        // setUser(null); // Assume user is logged out on error
      }
}

export async function get_user_info() {
    const oauthUserInfo = await get_oauth_user_info();
    console.log(oauthUserInfo);
    try {
        const response = await fetch('http://localhost:8080/users/email/'+oauthUserInfo.email);
        const userInfo = await response.json();
        
        return userInfo;
    }
    catch (error) {
        console.error('Error fetching user info:', error);
        return null;
    }
}