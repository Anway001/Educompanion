import React, { useState } from 'react';
import '../styles/VisualsPage.css';
import UserBadge from './UserBadge';

const VisualsPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [visuals, setVisuals] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [extractedText, setExtractedText] = useState('');

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

      console.debug('[VisualsPage] Sending POST to /visuals/generate', { file: selectedFile.name });
      const response = await fetch('http://localhost:8080/api/visuals/generate', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      if (!response.ok) {
        let bodyText = '';
        try {
          const json = await response.json();
          bodyText = json.error || json.message || JSON.stringify(json);
        } catch (e) {
          try { bodyText = await response.text(); } catch (e2) { bodyText = response.statusText || 'Unknown error'; }
        }
        console.debug('[VisualsPage] Server error response', { status: response.status, body: bodyText });
        throw new Error(bodyText || `Server responded with status ${response.status}`);
      }

      const data = await response.json();

      // Normalize returned paths: make them full URLs
      // Normalize returned paths: make them full URLs
      
        const normalize = (p) => {
          if (!p) return null;
          if (p.startsWith('http')) return p;
          return `http://localhost:8080${p.startsWith('/') ? p : '/' + p}`;
        };

        const normalizedVisuals = {
          bar_chart: normalize(data.bar_chart),
          pie_chart: normalize(data.pie_chart),
          flowchart: normalize(data.flowchart),
        };
      setVisuals(normalizedVisuals);

      if (data.extracted_text) {
        setStatusMessage('Text extracted from the file. Visuals generated.');
        setExtractedText(data.extracted_text);
      } else {
        setStatusMessage('Visuals generated successfully!');
      }
    } catch (error) {
      console.error('Error:', error);
      alert(`Error: ${error.message}`);
      setStatusMessage('Failed to generate visuals. Check console for details.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="podcast-content">
      <div className="page-background"></div>

      <header className="podcast-header">
        <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', width:'100%' }}>
          <div>
            <h1>Visuals Generator</h1>
            <p>Upload a PDF or image to generate flowcharts and graphs.</p>
          </div>
          <UserBadge />
        </div>
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
            {visuals.bar_chart && <img src={visuals.bar_chart} alt="Bar Chart" />}
            {visuals.pie_chart && <img src={visuals.pie_chart} alt="Pie Chart" />}
            {visuals.flowchart && <img src={visuals.flowchart} alt="Flowchart" />}
          </div>
        </div>
      )}

      {extractedText && (
        <div className="extracted-text">
          <hr className="divider" />
          <h3>Extracted Text</h3>
          <pre style={{ whiteSpace:'pre-wrap' }}>{extractedText}</pre>
        </div>
      )}
    </div>
  );
};

export default VisualsPage;
