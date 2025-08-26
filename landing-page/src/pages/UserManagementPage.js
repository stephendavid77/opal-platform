import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Table, Button, Alert } from 'react-bootstrap';

const UserManagementPage = () => {
    const [users, setUsers] = useState([]);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);

    const fetchUsers = async () => {
        try {
            // Replace with your actual API endpoint
            const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/users`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setUsers(data);
        } catch (error) {
            setError('Failed to fetch users: ' + error.message);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handleDelete = async (userId) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            try {
                // Replace with your actual API endpoint
                const accessToken = localStorage.getItem('access_token'); // Retrieve token

                const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/auth/users/${userId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                setMessage('User deleted successfully!');
                fetchUsers(); // Refresh the list
            } catch (error) {
                setError('Failed to delete user: ' + error.message);
            }
        }
    };

    return (
        <Container className="mt-4">
            <Row>
                <Col>
                    <h2>User Management</h2>
                    {error && <Alert variant="danger">{error}</Alert>}
                    {message && <Alert variant="success">{message}</Alert>}
                    <Table striped bordered hover responsive>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Active</th> {/* New header */}
                                <th>First Name</th> {/* New header */}
                                <th>Last Name</th> {/* New header */}
                                <th>Roles</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map((user) => (
                                <tr key={user.id}>
                                    <td>{user.id}</td>
                                    <td>{user.username}</td>
                                    <td>{user.email}</td>
                                    <td>{user.is_active ? 'Yes' : 'No'}</td> {/* New data cell */}
                                    <td>{user.first_name}</td> {/* New data cell */}
                                    <td>{user.last_name}</td> {/* New data cell */}
                                    <td>{user.roles}</td>
                                    <td>
                                        <Button
                                            variant="danger"
                                            size="sm"
                                            onClick={() => handleDelete(user.id)}
                                        >
                                            Delete
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </Col>
            </Row>
        </Container>
    );
};

export default UserManagementPage;