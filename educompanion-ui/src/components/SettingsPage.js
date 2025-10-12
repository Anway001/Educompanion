import React from 'react';
import '../styles/SettingsPage.css';

const SettingsPage = () => {
  return (
    <div className="settings-content">
      {/* Animated Background */}
      <div className="page-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
        <div className="floating-shape shape-4"></div>
      </div>

      <header className="settings-header">
        <div className="user-info">
          <span>Ananda Faris</span>
        </div>
      </header>
      <div className="welcome-section">
        <h1>Settings & Preferences</h1>
        <h2>Customize Your Experience</h2>
        <p>Manage your account settings, preferences, and configurations for EduCompanion.</p>
      </div>
    </div>
  );
};

export default SettingsPage;
