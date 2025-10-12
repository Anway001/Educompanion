import React, { useState } from 'react';
import '../styles/VideosPage.css';

const VideosPage = () => {
  const [uploadMode, setUploadMode] = useState('upload');
  const [selectedFiles, setSelectedFiles] = useState([]);

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

  return (
    <div className="videos-content">
      {/* Animated Background */}
      <div className="page-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
        <div className="floating-shape shape-4"></div>
      </div>

      <header className="videos-header">
        <div className="user-info">
          <span>Ananda Faris</span>
        </div>
      </header>
      
      <div className="welcome-section">
        <h1>Video Library</h1>
        <h2>Watch and Create Video Content</h2>
        <p>Access your video library, create video content, and explore educational videos with EduCompanion.</p>
      </div>

      {/* File Upload Section */}
      <div className="upload-section">
        <p className="upload-description">and we'll work our magic to create something awesome for you.</p>
        
        {/* Toggle Buttons */}
        <div className="upload-toggle">
          <button 
            className={`toggle-btn ${uploadMode === 'upload' ? 'active' : ''}`}
            onClick={() => setUploadMode('upload')}
          >
            Upload Videos
          </button>
          <button 
            className={`toggle-btn ${uploadMode === 'notes' ? 'active' : ''}`}
            onClick={() => setUploadMode('notes')}
          >
            Type Notes
          </button>
        </div>

        {/* File Upload Area */}
        {uploadMode === 'upload' && (
          <div className="file-upload-area">
            <div 
              className="drop-zone"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              <div className="upload-icon">📁</div>
              <h3>Drop your video files here</h3>
              <p>or click to browse files</p>
              <input
                type="file"
                multiple
                accept="video/*"
                onChange={handleFileSelect}
                className="file-input"
                id="video-file-input"
              />
              <label htmlFor="video-file-input" className="choose-files-btn">
                Choose Files
              </label>
            </div>
          </div>
        )}

        {/* Notes Input Area */}
        {uploadMode === 'notes' && (
          <div className="notes-input-area">
            <textarea 
              placeholder="Type your notes here..."
              className="notes-textarea"
            />
          </div>
        )}

        {/* Submit Button */}
        <button className="submit-btn">Let's Make Something Cool!</button>
      </div>
    </div>
  );
};

export default VideosPage;
