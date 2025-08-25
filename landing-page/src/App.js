import React from 'react';
import './App.css';

function App() {
  const applications = [
    { name: 'RegressionInsight', url: '/regression-insight' },
    { name: 'StandupBot', url: '/standup-bot' },
    { name: 'BuildPilot', url: '/build-pilot' },
    { name: 'CalMind', url: '/cal-mind' },
    { name: 'MonitorIQ', url: '/monitor-iq' },
    { name: 'XrayQC', url: '/xray-qc' },
  ];

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
          <h2>Login</h2>
          <p>
            This section can be integrated with a central login module.
            <br />
            (e.g., OAuth, JWT-based authentication)
          </p>
          {/* Placeholder for a login form or button */}
          <button onClick={() => alert('Login functionality to be integrated!')}>
            Login / Register
          </button>
        </section>
      </main>
      <footer>
        <p>&copy; 2025 OpalSuite. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
