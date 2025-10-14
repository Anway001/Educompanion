import React, { useState } from 'react';
import '../styles/SummarizePage.css';
import UserBadge from './UserBadge';

const SummarizerPage = () => {
  const [uploadMode, setUploadMode] = useState('upload');
  const [selectedFile, setSelectedFile] = useState(null);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [summary, setSummary] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setSelectedFile(file);
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleTextChange = (e) => setInputText(e.target.value);

  const handleSubmit = async () => {
    setIsLoading(true);
    setSummary('');
    setStatusMessage('Preparing to summarize...');

    const formData = new FormData();

    if (uploadMode === 'upload') {
      if (!selectedFile) {
        alert('Please select a file to upload.');
        setIsLoading(false);
        return;
      }
      formData.append('file', selectedFile);
    } else if (uploadMode === 'text') {
      if (!inputText.trim()) {
        alert('Please enter some text to summarize.');
        setIsLoading(false);
        return;
      }
      formData.append('text', inputText);
    }

    try {
      setStatusMessage('Sending data to server...');
      const response = await fetch('http://localhost:8080/api/summarizer/summarize', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to summarize the content.');
      }

      const data = await response.json();
      setSummary(data.summary);
      setStatusMessage('Summarization complete!');
    } catch (error) {
      console.error('Error:', error);
      setStatusMessage(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(summary);
    alert('Summary copied to clipboard!');
  };

  const handleDownload = () => {
    const blob = new Blob([summary], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `summary_${Date.now()}.txt`;
    link.click();
  };

  return (
    <div className="summarize-content">
      <div className="page-background">
        <div className="floating-shape shape-1"></div>
        <div className="floating-shape shape-2"></div>
        <div className="floating-shape shape-3"></div>
        <div className="floating-shape shape-4"></div>
      </div>

      <header className="summarize-header">
        <UserBadge />
      </header>

      <div className="welcome-section">
        <h1>AI Document Summarizer</h1>
        <h2>Upload a PDF or Paste Text to Get a Smart Summary</h2>
        <p>Powered by advanced AI summarization and OCR for scanned files.</p>
      </div>

      <div className="upload-section">
        <p className="upload-description">Upload your document or enter your own text to summarize.</p>

        <div className="upload-toggle">
          <button
            className={`toggle-btn ${uploadMode === 'upload' ? 'active' : ''}`}
            onClick={() => {
              setUploadMode('upload');
              setInputText('');
            }}
          >
            Upload File
          </button>
          <button
            className={`toggle-btn ${uploadMode === 'text' ? 'active' : ''}`}
            onClick={() => {
              setUploadMode('text');
              setSelectedFile(null);
            }}
          >
            Type Text
          </button>
        </div>

        {uploadMode === 'upload' && (
          <div className="file-upload-area" onDrop={handleDrop} onDragOver={handleDragOver}>
            <div className="drop-zone">
              <div className="upload-icon">📄</div>
              <h3>Drop your PDF here</h3>
              <p>or click to browse</p>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="file-input"
                id="file-input"
              />
              <label htmlFor="file-input" className="choose-file-btn">
                Choose File
              </label>
            </div>
            {selectedFile && <p>Selected file: {selectedFile.name}</p>}
          </div>
        )}

        {uploadMode === 'text' && (
          <div className="notes-input-area">
            <textarea
              placeholder="Paste or type text here..."
              className="notes-textarea"
              value={inputText}
              onChange={handleTextChange}
            />
          </div>
        )}

        <button className="submit-btn" onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Summarizing...' : 'Generate Summary'}
        </button>

        {isLoading && <p className="status-message">{statusMessage}</p>}

        <hr className="divider" />

{summary && (
  <div className="summary-container-v2">
    <h2 className="summary-title">Summary</h2>
    <div className="summary-display-v2">{summary}</div>
    <div className="summary-actions-v2">
      <button onClick={handleCopy} className="action-btn-v2 copy-btn-v2">Copy</button>
      <button onClick={handleDownload} className="action-btn-v2 download-btn-v2">Download</button>
    </div>
  </div>
)}
      </div>
    </div>
  );
};

export default SummarizerPage;
