import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/MainContent.css';

const MainContent = () => {
  const [inputValue, setInputValue] = useState('');
  const [user, setUser] = useState(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // ✅ Redirect if no user found in localStorage
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    } else {
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      navigate('/chat', { state: { message: inputValue } });
    }
  };

  const handleLogout = () => {
    // ✅ Clear user session and redirect immediately
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    
    window.location.href = "/login";
  };

  return (
    <div className="main-content">
      {/* Animated Background */}
      <div className="page-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
        <div className="floating-shape shape-4"></div>
      </div>

      <header className="main-header">
        <div 
          className="user-info" 
          onClick={() => setDropdownOpen(!dropdownOpen)} 
          style={{ position: "relative", cursor: "pointer" }}
        >
          <span>{user && `${user.first_name} ${user.last_name}`}</span>
          
          {dropdownOpen && (
            <div className="dropdown-menu">
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </header>

      <div className="welcome-section">
        <h1>Hi, {user && `${user.first_name} ${user.last_name}`}!</h1>
        <h2>How can we help you today?</h2>
        <p>Let's get started in a few simple steps, we'll show you how to use EduCompanion to unlock your productivity.</p>
      </div>

      <div className="chat-section">
        <div className="quick-actions">
          <button>I need a video form of my notes</button>
          <button>I want a podcast from my notes</button>
          <button>I need a notes format of any video</button>
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Send Aletheia a message"
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>

      <div className="features-grid">
        <div className="feature-card">
          <h3>Generate Podcasts from Notes</h3>
          <p>Enter your command to instantly generate Podcasts from your notes.</p>
        </div>
        <div className="feature-card">
          <h3>Generate Notes from any Youtube videos</h3>
          <p>Provide your video link, and EduCompanion will draft precise notes.</p>
        </div>
        <div className="feature-card">
          <h3>Generate Videos from notes</h3>
          <p>Input your Handwritten notes or Printed notes, and let the AI create video content.</p>
        </div>
        <div className="feature-card">
          <h3>Chat with EduCompanion</h3>
          <p>Generate responses to your queries in real-time.</p>
        </div>
      </div>
    </div>
  );
};

export default MainContent;
