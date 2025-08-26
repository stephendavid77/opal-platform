import React, { useState, useEffect } from 'react'; // Import useEffect
import { Container, Form, Button, Alert, Card, Row } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom'; // Import useLocation

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
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
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Registration failed');
            }

            setMessage('Registration successful! Please check your email for an OTP to activate your account.');
            setRegistrationSuccess(true); // Set success state to true
            localStorage.setItem('registeredEmail', email); // Store email in local storage
        } catch (err) {
            setError(err.message);
        }
    };

    const [otpCode, setOtpCode] = useState('');
    const handleResendOtp = async () => { // New function
        setMessage(null);
        setError(null);
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/request-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to resend OTP');
            }

            setMessage('New OTP sent to your email. Please check your inbox.');
        } catch (err) {
            setError(err.message);
        }
    };
    const handleOtpSubmit = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/activate-account`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, otp_code: otpCode }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'OTP verification failed');
            }

            setMessage('Account activated successfully! You can now log in.');
            setOtpCode(''); // Clear OTP field
            // Optionally, redirect to login page
            // Add a link to login page
            setError(
                <>
                    Account activated successfully! You can now log in.
                    <br />
                    <Link to="/login">Click here to go to Login Page</Link>
                </>
            );
        } catch (err) {
            setError(err.message);
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