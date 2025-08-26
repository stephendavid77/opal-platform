import React, { useState, useEffect } from 'react'; // Import useEffect
import { Container, Form, Button, Alert, Card, Row } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate
import { jwtDecode } from 'jwt-decode'; // Import jwtDecode

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false); // New state for login status
    const [isSuperuser, setIsSuperuser] = useState(false); // New state for superuser status

    const navigate = useNavigate(); // Get navigate function

    useEffect(() => {
        // Check login status on component mount
        const accessToken = localStorage.getItem('access_token');
        if (accessToken) {
            setIsLoggedIn(true);
            try {
                const decodedToken = jwtDecode(accessToken);
                if (decodedToken.roles && decodedToken.roles.includes("super_user")) {
                    setIsSuperuser(true);
                }
            } catch (decodeError) {
                console.error("Failed to decode JWT token from localStorage:", decodeError);
                // Clear invalid token
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_roles');
                setIsLoggedIn(false);
                setIsSuperuser(false);
            }
        }
    }, []); // Run once on mount

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            const details = {
                'username': username,
                'password': password
            };

            const formBody = Object.keys(details).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key])).join('&');

            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formBody,
            });

            const data = await response.json();

            if (!response.ok) {
                if (data.detail === "Account is not active. Please activate your account via OTP.") {
                    setError(
                        <>
                            Account is not active. Please check your email for OTP and activate your account.
                            <br />
                            <Link to="/register?activate=true">Click here to activate your account</Link>
                        </>
                    );
                } else {
                    throw new Error(data.detail || 'Login failed');
                }
                return; // Stop execution if account is inactive
            }

            // Store the token and roles (e.g., in localStorage)
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);

            // Decode the access token to get user roles
            try {
                const decodedToken = jwtDecode(data.access_token);
                if (decodedToken.roles) {
                    localStorage.setItem('user_roles', decodedToken.roles);
                    if (decodedToken.roles.includes("super_user")) {
                        setIsSuperuser(true);
                    }
                }
            } catch (decodeError) {
                console.error("Failed to decode JWT token:", decodeError);
                // Clear invalid token
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_roles');
                setIsLoggedIn(false);
                setIsSuperuser(false);
            }

            setMessage('Login successful!');
            setIsLoggedIn(true); // Update login state
            setUsername('');
            setPassword('');
            navigate('/dashboard'); // Redirect to dashboard
        } catch (err) {
            setError(err.message);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_roles');
        setIsLoggedIn(false);
        setIsSuperuser(false);
        setMessage('Logged out successfully.');
    };

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
            <Row className="justify-content-center">
                <Card className="p-4 shadow" style={{ maxWidth: '400px' }}>
                    <Card.Body>
                        <h2 className="text-center mb-4">Login</h2>
                        {message && <Alert variant="success">{message}</Alert>}
                        {error && <Alert variant="danger">{error}</Alert>}

                        {isLoggedIn ? ( // Conditionally render based on login status
                            <div>
                                <p className="text-center">You are logged in.</p>
                                {isSuperuser && (
                                    <p className="text-center mt-3">
                                        <Link to="/manage/users">Manage Users</Link>
                                    </p>
                                )}
                                <Button variant="danger" onClick={handleLogout} className="w-100 mt-3">
                                    Logout
                                </Button>
                            </div>
                        ) : (
                            <Form onSubmit={handleSubmit}>
                                <Form.Group className="mb-3" controlId="formBasicUsername">
                                    <Form.Label>Username</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Enter username"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        required
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3" controlId="formBasicPassword">
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                    />
                                </Form.Group>

                                <Button variant="primary" type="submit" className="w-100 mt-3">
                                    Login
                                </Button>
                                <p className="text-center mt-3">
                                    <Link to="/forgot-password">Forgot Password?</Link>
                                </p>
                                <p className="text-center mt-3">
                                    Don't have an account? <Link to="/register">Register here</Link>
                                </p>
                            </Form>
                        )}
                    </Card.Body>
                </Card>
            </Row>
        </Container>
    );
};

export default LoginPage;