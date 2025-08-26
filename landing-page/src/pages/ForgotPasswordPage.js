import React, { useState } from 'react';
import { Container, Form, Button, Alert, Card, Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const ForgotPasswordPage = () => {
    const [email, setEmail] = useState('');
    const [otpCode, setOtpCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);
    const [otpSent, setOtpSent] = useState(false);

    const handleRequestOtp = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/request-password-reset-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to request OTP');
            }

            setMessage('OTP sent to your email. Please check your inbox.');
            setOtpSent(true);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();
        setMessage(null);
        setError(null);

        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/reset-password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, otp_code: otpCode, new_password: newPassword }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to reset password');
            }

            setMessage('Password reset successfully! You can now log in with your new password.');
            setEmail('');
            setOtpCode('');
            setNewPassword('');
            setOtpSent(false); // Reset form
        } catch (err) {
            setError(err.message);
        }
    };

    const handleResendOtp = async () => { // Moved this function here
        setMessage(null);
        setError(null);
        try {
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/request-password-reset-otp`, {
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

    return (
        <Container className="d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
            <Row className="justify-content-center">
                <Card className="p-4 shadow" style={{ maxWidth: '400px' }}>
                    <Card.Body>
                        <h2 className="text-center mb-4">Forgot Password</h2>
                        {message && <Alert variant="success">{message}</Alert>}
                        {error && <Alert variant="danger">{error}</Alert>}

                        {!otpSent ? (
                            <Form onSubmit={handleRequestOtp}>
                                <Form.Group className="mb-3" controlId="formBasicEmail">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control
                                        type="email"
                                        placeholder="Enter your email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                    />
                                </Form.Group>
                                <Button variant="primary" type="submit" className="w-100 mt-3">
                                    Request OTP
                                </Button>
                            </Form>
                        ) : (
                            <Form onSubmit={handleResetPassword}>
                                <Form.Group className="mb-3" controlId="formBasicEmail">
                                    <Form.Label>Email address</Form.Label>
                                    <Form.Control
                                        type="email"
                                        placeholder="Enter your email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        disabled // Email should be disabled after OTP request
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
                                <Form.Group className="mb-3" controlId="formBasicNewPassword">
                                    <Form.Label>New Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        placeholder="Enter new password"
                                        value={newPassword}
                                        onChange={(e) => setNewPassword(e.target.value)}
                                        required
                                    />
                                </Form.Group>
                                <Button variant="success" type="submit" className="w-100 mt-3">
                                    Reset Password
                                </Button>
                                <Button variant="link" onClick={handleResendOtp} className="w-100 mt-2"> 
                                    Resend OTP
                                </Button>
                            </Form>
                        )}
                        <p className="text-center mt-3">
                            <Link to="/login">Back to Login</Link>
                        </p>
                    </Card.Body>
                </Card>
            </Row>
        </Container>
    );
};

export default ForgotPasswordPage;