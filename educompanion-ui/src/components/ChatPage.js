import React, { useState, useEffect, useRef } from 'react';
import '../styles/ChatPage.css';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [user, setUser] = useState(null);
  const msgsRef = useRef(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) setUser(JSON.parse(stored));
  }, []);

  useEffect(() => {
    // scroll to bottom on new message
    if (msgsRef.current) msgsRef.current.scrollTop = msgsRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const outgoing = { from: 'you', text: input, ts: new Date().toISOString() };
    setMessages((m) => [...m, outgoing]);

    // call backend chat endpoint
    const token = localStorage.getItem('access_token');
    try {
      const res = await fetch('/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({ message: input })
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        const text = err.error || err.message || `HTTP ${res.status}`;
        setMessages((m) => [...m, { from: 'system', text: `Error: ${text}`, ts: new Date().toISOString() }]);
      } else {
        const json = await res.json();
        setMessages((m) => [...m, { from: 'bot', text: json.reply, ts: json.timestamp }]);
      }
    } catch (e) {
      setMessages((m) => [...m, { from: 'system', text: `Network error: ${e.message}`, ts: new Date().toISOString() }]);
    }

    setInput('');
  };

  return (
    <div className="chat-page-container">
      <div className="chat-header">
        <h1>Chat with EduCompanion</h1>
        <div className="user-badge">{user ? `${user.first_name} ${user.last_name}` : 'Guest'}</div>
      </div>

      <div className="chat-messages" ref={msgsRef}>
        {messages.map((m, i) => (
          <div key={i} className={`chat-message ${m.from}`}>
            <div className="meta">{m.from}</div>
            <div className="text">{m.text}</div>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask Aletheia anything..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatPage;
