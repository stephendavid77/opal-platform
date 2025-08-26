import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const tools = [
    { name: 'BuildPilot', icon: '🚀', path: '/buildpilot' },
    { name: 'CalMind', icon: '🧠', path: '/calmind' },
    { name: 'MonitorIQ', icon: '📊', path: '/monitoriq' },
    { name: 'RegressionInsight', icon: '🔍', path: '/regressioninsight' },
    { name: 'StandupBot', icon: '🤖', path: '/standupbot' },
    { name: 'XrayQC', icon: '🔬', path: '/xrayqc' },
];

const DashboardPage = () => {
    return (
        <Container className="mt-5">
            <h2 className="text-center mb-4">Welcome to OpalSuite!</h2>
            <p className="text-center mb-5">Select a tool to get started:</p>
            <Row className="justify-content-center">
                {tools.map((tool) => (
                    <Col key={tool.name} xs={6} sm={4} md={3} lg={2} className="mb-4">
                        <Link to={tool.path} style={{ textDecoration: 'none' }}>
                            <Card className="text-center p-3 shadow-sm h-100 d-flex flex-column justify-content-center align-items-center">
                                <div style={{ fontSize: '3em', marginBottom: '10px' }}>{tool.icon}</div>
                                <Card.Title>{tool.name}</Card.Title>
                            </Card>
                        </Link>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default DashboardPage;