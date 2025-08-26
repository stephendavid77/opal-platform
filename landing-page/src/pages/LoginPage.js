import React, { useState, useEffect } from 'react'; // Import useEffect
import { Container, Form, Button, Alert, Card, Row } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate
import { jwtDecode } from 'jwt-decode'; // Import jwtDecode

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [otpSent, setOtpSent] = useState(false);
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

    const handleRequestOtp = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            console.log("Requesting OTP for email:", email);
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/request-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });
            console.log("OTP Request Response:", response);
            const data = await response.json();
            console.log("OTP Request Response Data:", data);

            if (!response.ok) {
                throw new Error(JSON.stringify(data.detail) || 'Failed to request OTP');
            }

            setMessage(JSON.stringify(data.message) || 'OTP sent to your email!');
            setOtpSent(true);
        } catch (err) {
            setError(String(err));
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            console.log("Attempting login with email:", email, "and OTP:", otp);
            const details = {
                'email': email,
                'otp': otp
            };

            const formBody = Object.keys(details).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key])).join('&');

            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/login-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, otp }),
            });
            console.log("Login Response:", response);
            const data = await response.json();
            console.log("Login Response Data:", data);

            if (!response.ok) {
                throw new Error(JSON.stringify(data.detail) || 'Login failed');
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
            setEmail('');
            setOtp('');
            setOtpSent(false); // Reset OTP sent state
            navigate('/portal'); // Redirect to portal
        } catch (err) {
            setError(String(err));
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
                            <Form onSubmit={otpSent ? handleLogin : handleRequestOtp}>
                                <Form.Group className="mb-3" controlId="formBasicEmail">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control
                                        type="email"
                                        placeholder="Enter email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        disabled={otpSent} // Disable email input after OTP is sent
                                    />
                                </Form.Group>

                                {otpSent && (
                                    <Form.Group className="mb-3" controlId="formBasicOtp">
                                        <Form.Label>OTP</Form.Label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Enter OTP"
                                            value={otp}
                                            onChange={(e) => setOtp(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                )}

                                <Button variant="primary" type="submit" className="w-100 mt-3">
                                    {otpSent ? 'Login with OTP' : 'Request OTP'}
                                </Button>
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