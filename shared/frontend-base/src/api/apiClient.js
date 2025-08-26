import { useNavigate } from 'react-router-dom';

const getAuthHeaders = () => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        return {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        };
    }
    return { 'Content-Type': 'application/json' };
};

const apiClient = async (url, options = {}) => {
    const headers = {
        ...getAuthHeaders(),
        ...options.headers,
    };

    const response = await fetch(url, { ...options, headers });

    if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
            // Handle token expiration or invalid token globally
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_roles');
            // Redirect to login page - this part needs to be handled carefully in a global utility
            // For now, we'll just throw an error and let the calling component handle redirection
            throw new Error('Unauthorized or Forbidden. Please log in again.');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
};

export default apiClient;
