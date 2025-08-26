import React, { useState } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const applications = [
    { name: 'RegressionInsight', url: '/regression-insight' },
    { name: 'StandupBot', url: '/standup-bot' },
    { name: 'BuildPilot', url: '/build-pilot' },
    { name: 'CalMind', url: '/cal-mind' },
    { name: 'MonitorIQ', url: '/monitor-iq' },
    { name: 'XrayQC', url: '/xray-qc' },
  ];

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState(''); // New state for email
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);
  const [isRegistering, setIsRegistering] = useState(false); // New state to toggle between login/register

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch(`${API_URL}/auth/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      setToken(data.access_token);
    } catch (error) {
      setError(error.message);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          email,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
      }

      const data = await response.json();
      setToken(data.access_token);
      alert('Registration successful! You are now logged in.');
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to OpalSuite</h1>
        <p>Your centralized hub for all applications.</p>
      </header>
      <main>
        <section className="app-list">
          <h2>Available Applications</h2>
          <ul>
            {applications.map((app) => (
              <li key={app.name}>
                <a href={app.url} target="_blank" rel="noopener noreferrer">
                  {app.name}
                </a>
              </li>
            ))}
          </ul>
        </section>
        <section className="login-section">
          <h2>{isRegistering ? 'Register' : 'Login'}</h2>
          {token ? (
            <div>
              <p>Login successful!</p>
              <p>Token: {token}</p>
              <button onClick={() => setToken(null)}>Logout</button>
            </div>
          ) : (
            <>
              {error && <p className="error">{error}</p>}
              <form onSubmit={isRegistering ? handleRegister : handleLogin}>
                <div>
                  <label htmlFor="username">Username</label>
                  <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label htmlFor="password">Password</label>
                  <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                {isRegistering && (
                  <div>
                    <label htmlFor="email">Email</label>
                    <input
                      type="email"
                      id="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                )}
                <button type="submit">
                  {isRegistering ? 'Register' : 'Login'}
                </button>
              </form>
              <p>
                {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
                <button onClick={() => setIsRegistering(!isRegistering)}>
                  {isRegistering ? 'Login' : 'Register'}
                </button>
              </p>
            </>
          )}
        </section>
      </main>
      <footer>
        <p>&copy; 2025 OpalSuite. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;