import React, { useState, useEffect } from 'react';
import '../styles/NotesPage.css';

const NotesPage = () => {
  const [notes, setNotes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchNotes = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // MODIFIED: Get the token directly from 'access_token' in localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error("Authentication Error: Please log in to view your notes.");
      }

      const response = await fetch('http://localhost:8080/api/podcast/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Could not fetch your notes from the server.');
      }
      
      const data = await response.json();
      setNotes(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  return (
    <div className="notes-content">
       {/* ... The rest of your JSX is perfect and does not need to be changed ... */}
       {/* (header, welcome-section, action-bar, stats-section, etc.) */}
      <div className="page-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
      </div>
      <header className="notes-header">
        <div className="user-info">
          <span>Ananda Faris</span>
        </div>
      </header>
      <div className="welcome-section">
        <h1 className="gradient-text flash-effect">Notes & Documentation</h1>
        <h2 className="gradient-text">Organize Your Thoughts</h2>
        <p>Create, edit, and organize your notes with EduCompanion's powerful note-taking features.</p>
      </div>
      <div className="action-bar">
        <button className="btn btn-primary glow-hover">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            Create New Note
        </button>
        <button className="btn btn-secondary glow-hover">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            Search Notes
        </button>
      </div>
      <div className="content-grid">
        {isLoading && <p className="loading-message">Loading your notes...</p>}
        {error && <p className="error-message">Error: {error}</p>}
        {!isLoading && !error && notes.length === 0 && (
            <p className="loading-message">No podcasts saved yet. Go create one!</p>
        )}
        {!isLoading && !error && notes.map((note) => (
          <div key={note.id} className="content-card glow-hover flash-effect">
            <div className="card-header">
              <h3>{note.title}</h3>
              <span className="date">{note.date}</span>
            </div>
            <div className="card-content">
              <p>{note.preview}</p>
            </div>
            <div className="card-actions">
              <button className="btn btn-small btn-primary">Edit</button>
              <button className="btn btn-small btn-secondary">Share</button>
            </div>
          </div>
        ))}
      </div>
      <div className="stats-section">
        <div className="stats-grid">
            <div className="stat-card flash-effect">
                <div className="stat-number gradient-text">{notes.length}</div>
                <div className="stat-label">Total Notes</div>
            </div>
            <div className="stat-card flash-effect">
                <div className="stat-number gradient-text">8</div>
                <div className="stat-label">This Week</div>
            </div>
            <div className="stat-card flash-effect">
                <div className="stat-number gradient-text">156</div>
                <div className="stat-label">Study Hours</div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default NotesPage;