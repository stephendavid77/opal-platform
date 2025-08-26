import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UserManagementPage from './pages/UserManagementPage';
import LoginPage from './pages/LoginPage'; // Import LoginPage
import RegisterPage from './pages/RegisterPage'; // Import RegisterPage
import ForgotPasswordPage from './pages/ForgotPasswordPage'; // Import ForgotPasswordPage
import DashboardPage from './pages/DashboardPage'; // Import DashboardPage
import PortalPage from './pages/PortalPage'; // Import PortalPage
import NavigationBar from './components/NavigationBar'; // Import NavigationBar
import './App.css';

function App() {
  return (
    <Router>
      <NavigationBar /> {/* Render NavigationBar here */}
      <Routes>
        <Route path="/manage/users" element={<UserManagementPage />} />
        <Route path="/login" element={<LoginPage />} /> {/* New Login Route */}
        <Route path="/register" element={<RegisterPage />} /> {/* New Register Route */}
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/dashboard" element={<DashboardPage />} /> {/* New Dashboard Route */}
        <Route path="/portal" element={<PortalPage />} /> {/* New Portal Page Route */}
        <Route path="/" element={<LoginPage />} /> {/* Make LoginPage the default route */}
      </Routes>
    </Router>
  );
}

export default App;