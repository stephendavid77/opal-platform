import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import UserManagementPage from './pages/UserManagementPage';
import LoginPage from './pages/LoginPage'; // Import LoginPage
import RegisterPage from './pages/RegisterPage'; // Import RegisterPage
import './App.css';

function App() {
  return (
    <Router>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">OpalSuite Landing</Link>
          <div className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link" to="/manage/users">Manage Users</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/login">Login</Link> {/* New Login Link */}
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/register">Register</Link> {/* New Register Link */}
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/manage/users" element={<UserManagementPage />} />
        <Route path="/login" element={<LoginPage />} /> {/* New Login Route */}
        <Route path="/register" element={<RegisterPage />} /> {/* New Register Route */}
        <Route path="/" element={
          <header className="App-header">
            <p>Welcome to OpalSuite!</p>
            <p>Navigate to <Link to="/manage/users">Manage Users</Link></p>
            <p>Or <Link to="/login">Login</Link> / <Link to="/register">Register</Link></p>
          </header>
        } />
      </Routes>
    </Router>
  );
}

export default App;