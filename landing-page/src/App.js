import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import UserManagementPage from './pages/UserManagementPage';
import LoginPage from './pages/LoginPage'; // Import LoginPage
import RegisterPage from './pages/RegisterPage'; // Import RegisterPage
import ForgotPasswordPage from './pages/ForgotPasswordPage'; // Import ForgotPasswordPage
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/manage/users" element={<UserManagementPage />} />
        <Route path="/login" element={<LoginPage />} /> {/* New Login Route */}
        <Route path="/register" element={<RegisterPage />} /> {/* New Register Route */}
        <Route path="/forgot-password" element={<ForgotPasswordPage />} /> {/* New Forgot Password Route */}
        <Route path="/" element={<LoginPage />} /> {/* Make LoginPage the default route */}
      </Routes>
    </Router>
  );
}

export default App;