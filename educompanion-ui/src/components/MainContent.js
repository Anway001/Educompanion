import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/MainContent.css';

const MainContent = () => {
  const [inputValue, setInputValue] = useState('');
  const [user, setUser] = useState(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
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

  // client-side predefined Q&A map so chat works even if backend is down
  const qaMap = {
    'hello': 'Hello! How can I help you today?',
    'hi': 'Hello! How can I help you today?',
    'hey': 'Hello! How can I help you today?',
    'i need a video': 'To create a video from your notes: go to the Videos page, paste or upload your notes, choose a template and press Generate. You can then download the MP4 or save it to your account.',
    'i want a podcast': 'To make a podcast: go to the Podcast page, upload your notes (or paste text), choose voice and length, then click Generate. After generation you can Save, Play, Download, or Share.',
    'how do i create a podcast': 'To create a podcast: go to the Podcast page, upload or provide notes, then click Generate. You can save the generated podcast to your account.',
    'how to upload notes': 'Use the Podcast or Videos page and select "Upload" or paste text into the input area. Supported formats: .txt, .md, and .pdf (for text extraction).',
    'where are my saved podcasts': 'Saved podcasts are visible on the Podcast page under "Saved Podcasts" — they are tied to your account.',
    'how to download a podcast': 'Open the saved podcast on the Podcast page and use the Download button to save the MP3 to your device.',
    'how to play saved podcast': 'Click the Play button next to a saved podcast to stream it directly in the app. If playback fails, ensure the file exists on the server or re-generate the podcast.',
    'how to save a podcast': 'After generating, choose "Save" or use the Save button on the podcast player to store it in your account.',
    'how to share a podcast': 'Open the saved podcast and use the Share button to create a public link you can send to others. Note: only podcasts with files can be shared.',
    'how do i change my password': 'Go to Settings -> Account and use the change password form to update your password.',
    'what formats are supported': 'We currently support MP3 audio for podcasts. Video notes can be exported as MP4.'
  };

  // helper to send quick-action phrases (used by buttons)
  const handleQuickAction = (phrase) => {
    // send phrase directly to handler (bypasses input state)
    handleSendMessage(phrase);
  };

  const handleSendMessage = (overrideMessage) => {
    const raw = overrideMessage !== undefined ? overrideMessage : inputValue;
    if (!raw || !raw.trim()) return;

    const message = raw.trim();
    // clear input only when user typed into it
    if (overrideMessage === undefined) setInputValue('');

    // append user's message to chat list in-page
    setChatMessages((m) => [...m, { from: 'you', text: message }]);

    // try to answer from client-side predefined QA map
    const normalized = message.toLowerCase();
    let reply = qaMap[normalized];
    if (!reply) {
      // substring-based matching
      for (const k of Object.keys(qaMap)) {
        if (normalized.includes(k)) {
          reply = qaMap[k];
          break;
        }
      }
    }

    if (!reply) {
      // fallback canned reply when no local match — avoids calling backend and causing HTTP 404
      reply = "Sorry, I don't have an answer for that yet. Try asking about creating, saving, or sharing podcasts.";
    }

    setChatMessages((m) => [...m, { from: 'bot', text: reply }]);
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
          <button onClick={() => handleQuickAction('i need a video')}>I need a video form of my notes</button>
          <button onClick={() => handleQuickAction('i want a podcast')}>I want a podcast from my notes</button>
          <button onClick={() => handleQuickAction('i need a notes format of any video')}>I need a notes format of any video</button>
        </div>

        
        <div className="chat-box">

          
          <div className="chat-messages-inline">
            {chatMessages.map((m, idx) => (
              <div key={idx} className={`chat-msg ${m.from}`}>
                <strong className="msg-from">{m.from}:</strong>&nbsp;<span className="msg-text">{m.text}</span>
              </div>
            ))}
            
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask Aletheia something..."
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            />
            <button onClick={() => handleSendMessage()}>Send</button>
          </div>
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
