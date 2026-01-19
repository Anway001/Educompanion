import React from 'react';
import '../styles/PodcastPage.css';
import UserBadge from './UserBadge';
import { usePodcastContext } from '../contexts/PodcastContext';

const PodcastPage = () => {
  const {
    uploadMode, setUploadMode,
    selectedFiles, setSelectedFiles, // We try to keep this, but if page unmounts file input value is lost. 
    notes, setNotes,
    length, setLength,
    isLoading, setIsLoading,
    podcastUrl, setPodcastUrl,
    statusMessage, setStatusMessage,
    generatedFilename, setGeneratedFilename
  } = usePodcastContext();

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    setSelectedFiles(files);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleNotesChange = (event) => {
    setNotes(event.target.value);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setPodcastUrl('');
    setStatusMessage('Starting podcast generation...');

    const formData = new FormData();
    formData.append('length', length);

    if (uploadMode === 'notes') {
      if (!notes) {
        alert("Please type some notes to generate a podcast.");
        setIsLoading(false);
        return;
      }
      formData.append('notes_text', notes);
    } else if (uploadMode === 'upload') {
      if (selectedFiles.length === 0) {
        alert("Please select a file to upload.");
        setIsLoading(false);
        return;
      }
      formData.append('file', selectedFiles[0]);
    }

    try {
      // MODIFIED: Get the token correctly from localStorage
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error("Authentication Error. Please log in again.");
      }

      setStatusMessage('Sending request to the server...');
      const response = await fetch('http://localhost:8080/api/podcast/generate', {
        method: 'POST',
        headers: {
          // MODIFIED: Send the token for authorization
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate podcast.');
      }

      // MODIFIED: Extract filename from headers to save it later
      const disposition = response.headers.get('Content-Disposition');
      let filename = null;
      if (disposition && disposition.indexOf('filename=') !== -1) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '');
        }
      }
      console.log("Captured generated filename:", filename);
      setGeneratedFilename(filename);

      setStatusMessage('Generating audio... this can take a few minutes.');
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setPodcastUrl(url);
      setStatusMessage('Podcast generated successfully!');

    } catch (error) {
      console.error('Error:', error);
      alert(`Error: ${error.message}`);
      setStatusMessage('Failed to generate podcast. Check console for details.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error("Authentication Error. Please log in again.");
      }

      const title = selectedFiles.length > 0
        ? selectedFiles[0].name.replace(/\.[^/.]+$/, "")
        : "Podcast from Notes";
      const date = new Date().toISOString().split('T')[0];

      // MODIFIED: Send the filename to the backend so it can link the file
      const metadata = {
        title,
        date,
        preview: "An AI-generated podcast.",
        filename: generatedFilename // Pass the captured filename
      };

      await fetch('http://localhost:8080/api/podcast/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(metadata),
      });
      setStatusMessage('Podcast saved to your notes!');
      alert("Podcast saved successfully to your library!");
    } catch (saveError) {
      setStatusMessage('Failed to save podcast to notes.');
    }
  };

  return (
    <div className="podcast-content">
      {/* ... The rest of your JSX is perfect and does not need to be changed ... */}
      {/* (header, welcome-section, upload-toggle, file-upload-area, notes-input-area, length-selector, etc.) */}
      <div className="page-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
        <div className="floating-shape shape-4"></div>
      </div>
      <header className="podcast-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div />
          <UserBadge />
        </div>
      </header>
      <div className="welcome-section">
        <h1>Podcast Hub</h1>
        <h2>Discover and Create Audio Content</h2>
        <p>Explore podcasts, create audio content, and manage your audio library with EduCompanion's podcast features.</p>
      </div>
      <div className="upload-section">
        <p className="upload-description">and we'll work our magic to create something awesome for you.</p>
        <div className="upload-toggle">
          <button className={`toggle-btn ${uploadMode === 'upload' ? 'active' : ''}`} onClick={() => { setUploadMode('upload'); setNotes(''); }}>
            Upload File
          </button>
          <button className={`toggle-btn ${uploadMode === 'notes' ? 'active' : ''}`} onClick={() => { setUploadMode('notes'); setSelectedFiles([]); }}>
            Type Notes
          </button>
        </div>
        {uploadMode === 'upload' && (
          <div className="file-upload-area">
            <div className="drop-zone" onDrop={handleDrop} onDragOver={handleDragOver}>
              <div className="upload-icon">📁</div>
              <h3>Drop your files here</h3>
              <p>or click to browse files</p>
              <input type="file" multiple={false} accept=".txt,.pdf" onChange={handleFileSelect} className="file-input" id="file-input" />
              <label htmlFor="file-input" className="choose-files-btn">Choose File</label>
            </div>
            {selectedFiles.length > 0 && (<p>Selected file: {selectedFiles[0].name}</p>)}
          </div>
        )}
        {uploadMode === 'notes' && (
          <div className="notes-input-area">
            <textarea placeholder="Type your notes here..." className="notes-textarea" value={notes} onChange={handleNotesChange} />
          </div>
        )}
        <div className="length-selector">
          <h4>Podcast Length</h4>
          <div className="length-toggle">
            <button className={`length-btn ${length === 'short' ? 'active' : ''}`} onClick={() => setLength('short')}>Short</button>
            <button className={`length-btn ${length === 'medium' ? 'active' : ''}`} onClick={() => setLength('medium')}>Medium</button>
            <button className={`length-btn ${length === 'long' ? 'active' : ''}`} onClick={() => setLength('long')}>Long</button>
          </div>
        </div>
        <button className="submit-btn" onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Generating...' : "Let's Make Something Cool!"}
        </button>
        {isLoading && (<p className="status-message">{statusMessage}</p>)}
        <hr className="divider" />
        {podcastUrl && (
          <div className="audio-player-container">
            <h3>Your Podcast is Ready!</h3>
            <audio controls src={podcastUrl} className="podcast-player"></audio>
            <a href={podcastUrl} download={`podcast_${Date.now()}.mp3`} className="download-btn">Download Podcast</a>
            <button onClick={handleSave} className="download-btn">Save Podcast</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PodcastPage;