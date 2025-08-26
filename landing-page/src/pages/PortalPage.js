import React, { useState, useEffect } from 'react'; // Import useState and useEffect
import { Container, Card, Row, Col, Button, Alert, Spinner } from 'react-bootstrap'; // Import Alert and Spinner
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import apiClient from '@opalsuite/frontend-base/src/api/apiClient'; // Import apiClient

const PortalPage = () => {
    const [tools, setTools] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // Initialize useNavigate

    useEffect(() => {
        const fetchTools = async () => {
            try {
                const data = await apiClient(`${process.env.REACT_APP_BACKEND_URL}/tools`);
                setTools(data);
            } catch (err) {
                setError(err.message);
                if (err.message.includes('Unauthorized') || err.message.includes('Forbidden')) {
                    navigate('/login'); // Redirect to login on auth errors
                }
            } finally {
                setLoading(false);
            }
        };

        fetchTools();
    }, [navigate]); // Add navigate to dependency array

    if (loading) {
        return (
            <Container className="mt-5 text-center">
                <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading tools...</span>
                </Spinner>
                <p>Loading tools...</p>
            </Container>
        );
    }

    if (error) {
        return (
            <Container className="mt-5">
                <Alert variant="danger">Error: {error}</Alert>
            </Container>
        );
    }

    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">Welcome to OpalSuite!</h2>
            <p className="text-center mb-5">Select a tool to get started:</p>
            <Row xs={1} md={2} lg={3} className="g-4">
                {tools.map((tool, idx) => (
                    <Col key={idx}>
                        <Card className="h-100 shadow-sm">
                            <Card.Body>
                                <Card.Title>{tool.name}</Card.Title>
                                <Card.Text>{tool.description}</Card.Text>
                                <Link to={tool.path}>
                                    <Button variant="primary">Launch {tool.name}</Button>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default PortalPage;