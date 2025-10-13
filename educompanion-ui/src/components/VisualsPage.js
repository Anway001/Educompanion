import React, { useState } from 'react';
import '../styles/VisualsPage.css';

const VisualsPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [visuals, setVisuals] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setSelectedFile(event.dataTransfer.files[0]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      alert('Please select a file to upload.');
      return;
    }

    setIsLoading(true);
    setVisuals(null);
    setStatusMessage('Uploading and processing file...');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('Authentication Error. Please log in again.');
      }

      const response = await fetch('http://localhost:8080/api/visuals/generate', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate visuals.');
      }

      const data = await response.json();
      setVisuals(data);
      setStatusMessage('Visuals generated successfully!');
    } catch (error) {
      console.error('Error:', error);
      alert(`Error: ${error.message}`);
      setStatusMessage('Failed to generate visuals. Check console for details.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="visuals-content">
      <div className="page-background"></div>
      <header className="visuals-header">
        <h1>Visuals Generator</h1>
        <p>Upload a PDF or image to generate flowcharts and graphs.</p>
      </header>
      <div className="upload-section">
        <div className="file-upload-area">
          <div className="drop-zone" onDrop={handleDrop} onDragOver={handleDragOver}>
            <div className="upload-icon">📁</div>
            <h3>Drop your file here</h3>
            <p>or click to browse</p>
            <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={handleFileSelect} className="file-input" id="file-input" />
            <label htmlFor="file-input" className="choose-files-btn">Choose File</label>
          </div>
          {selectedFile && (<p>Selected file: {selectedFile.name}</p>)}
        </div>
        <button className="submit-btn" onClick={handleSubmit} disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Generate Visuals'}
        </button>
        {isLoading && (<p className="status-message">{statusMessage}</p>)}
      </div>
      {visuals && (
        <div className="visuals-results">
          <hr className="divider" />
          <h3>Generated Visuals</h3>
          <div className="visuals-grid">
            {visuals.bar_chart && <img src={`http://localhost:8080/${visuals.bar_chart}`} alt="Bar Chart" />}
            {visuals.pie_chart && <img src={`http://localhost:8080/${visuals.pie_chart}`} alt="Pie Chart" />}
            {visuals.flowchart && <img src={`http://localhost:8080/${visuals.flowchart}`} alt="Flowchart" />}
          </div>
        </div>
      )}
    </div>
  );
};

export default VisualsPage;
