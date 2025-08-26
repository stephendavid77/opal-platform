import React, { useState, useEffect } from 'react'; // Import useEffect
import { Container, Form, Button, Alert, Card, Row } from 'react-bootstrap';
import { useLocation } from 'react-router-dom'; // Import useLocation
import { jwtDecode } from 'jwt-decode'; // Import jwtDecode

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);
    const [registrationSuccess, setRegistrationSuccess] = useState(false);

    const location = useLocation(); // Get location object

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        if (params.get('activate') === 'true') {
            setRegistrationSuccess(true);
            const storedEmail = localStorage.getItem('registeredEmail'); // Retrieve email
            if (storedEmail) {
                setEmail(storedEmail); // Pre-fill email
            }
        }
    }, [location]); // Re-run effect if location changes // New state

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            console.log("Registering user with username:", username, "and email:", email);
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email }),
            });
            console.log("Registration Response:", response);
            const data = await response.json();
            console.log("Registration Response Data:", data);

            if (!response.ok) {
                throw new Error(JSON.stringify(data.detail) || 'Registration failed');
            }

            setMessage(JSON.stringify(data.message) || 'Registration successful! Please check your email for an OTP to verify your account.');
            setRegistrationSuccess(true); // Set success state to true
            localStorage.setItem('registeredEmail', email); // Store email in local storage
        } catch (err) {
            setError(String(err));
        }
    };

    const [otpCode, setOtpCode] = useState('');
    const handleResendOtp = async () => { // New function
        setMessage(null);
        setError(null);
        try {
            console.log("Resending OTP for email:", email);
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/request-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });
            console.log("Resend OTP Response:", response);
            const data = await response.json();
            console.log("Resend OTP Response Data:", data);

            if (!response.ok) {
                throw new Error(JSON.stringify(data.detail) || 'Failed to resend OTP');
            }

            setMessage(JSON.stringify(data.message) || 'New OTP sent to your email. Please check your inbox.');
        } catch (err) {
            setError(String(err));
        }
    };
    const handleOtpSubmit = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            console.log("Attempting OTP verification with email:", email, "and OTP:", otpCode);
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, otp: otpCode }),
            });
            console.log("OTP Verification Response:", response);
            const data = await response.json();
            console.log("OTP Verification Response Data:", data);

            if (!response.ok) {
                throw new Error(JSON.stringify(data.detail) || 'OTP verification failed');
            }

            // Store the token and roles (e.g., in localStorage)
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);

            // Decode the access token to get user roles
            try {
                const decodedToken = jwtDecode(data.access_token);
                if (decodedToken.roles) {
                    localStorage.setItem('user_roles', decodedToken.roles);
                }
            } catch (decodeError) {
                console.error("Failed to decode JWT token:", decodeError);
                // Clear invalid token
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_roles');
            }

            setMessage(JSON.stringify(data.message) || 'Account verified and logged in successfully!');
            setOtpCode(''); // Clear OTP field
            // Redirect to dashboard
            window.location.href = '/portal'; // Use window.location.href for full page reload
        } catch (err) {
            setError(String(err));
        }
    };

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
            <Row className="justify-content-center"> {/* Add justify-content-center to Row */}
                <Card className="p-4 shadow" style={{ maxWidth: '400px' }}> {/* Add maxWidth for better control */}
                        <Card.Body>
                            <h2 className="text-center mb-4">Register</h2>
                            {message && <Alert variant="success">{message}</Alert>}
                            {error && <Alert variant="danger">{error}</Alert>}
                            {!registrationSuccess ? ( // Conditionally render registration form
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

                                    <Form.Group className="mb-3" controlId="formBasicEmail">
                                        <Form.Label>Email address</Form.Label>
                                        <Form.Control
                                            type="email"
                                            placeholder="Enter email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            required
                                        />
                                    </Form.Group>

                                    

                                    <Button variant="primary" type="submit" className="w-100 mt-3">
                                        Register
                                    </Button>
                                </Form>
                            ) : ( // Render OTP verification form
                                <Form onSubmit={handleOtpSubmit}>
                                    <Form.Group className="mb-3" controlId="formBasicEmail"> {/* Add email field */}
                                        <Form.Label>Email address</Form.Label>
                                        <Form.Control
                                            type="email"
                                            placeholder="Enter email"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                    <Form.Group className="mb-3" controlId="formBasicOtp">
                                        <Form.Label>OTP Code</Form.Label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Enter OTP"
                                            value={otpCode}
                                            onChange={(e) => setOtpCode(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                    <Button variant="success" type="submit" className="w-100 mt-3">
                                        Activate Account
                                    </Button>
                                    <p className="text-center mt-2">
                                        <Button variant="secondary" onClick={handleResendOtp} className="w-100">
                                            Resend OTP
                                        </Button>
                                    </p>
                                </Form>
                            )}
                        </Card.Body>
                </Card>
            </Row>
        </Container>
    );
};

export default RegisterPage;