import { replace } from "react-router-dom";

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
        navigate('/'); // Optional: Redirect to an error page
        return false;
    }
}


export async function redirectTo(route) {
    console.log('Redirecting...');
    window.location.href = 'http://localhost:8080'+route;
}
