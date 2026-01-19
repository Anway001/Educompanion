import React, { useState, useEffect } from 'react';
import '../styles/VideosPage.css';
import UserBadge from './UserBadge';

const VideosPage = () => {
  const [uploadMode, setUploadMode] = useState('upload');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState('');
  const [generatedVideo, setGeneratedVideo] = useState(null);
  const [uploadedFilePreview, setUploadedFilePreview] = useState(null);

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);

    // Create preview for the first file
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        // For image files, create object URL for preview
        const previewUrl = URL.createObjectURL(file);
        setUploadedFilePreview(previewUrl);
      } else if (file.type === 'application/pdf') {
        // For PDF files, we'll show a PDF icon with filename
        setUploadedFilePreview('pdf');
      }
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    setSelectedFiles(files);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async () => {
    if (uploadMode === 'text-to-animation' && selectedFiles.length > 0) {
      await processTextToAnimation();
    } else {
      // Handle other upload modes
      console.log('Other upload modes not implemented yet');
    }
  };

  const processTextToAnimation = async () => {
    if (selectedFiles.length === 0) {
      alert('Please select a file first');
      return;
    }

    const file = selectedFiles[0]; // Process first file for now
    const isPdf = file.name.toLowerCase().endsWith('.pdf');

    setIsProcessing(true);

    try {
      // Step 1: Upload file
      setProcessingStatus('Uploading file...');
      const formData = new FormData();
      formData.append('file', file);

      const uploadResponse = await fetch('http://localhost:8080/api/text-to-animation/upload', {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error('Upload failed');
      }

      const uploadData = await uploadResponse.json();
      console.log('Upload data:', uploadData);
      const fileId = uploadData.file_id;
      console.log('File ID:', fileId);

      // Step 2: Process file (different messages for PDF vs Image)
      if (isPdf) {
        setProcessingStatus('Converting PDF to images...');
        await new Promise(resolve => setTimeout(resolve, 1000)); // Brief pause for user feedback

        setProcessingStatus('Extracting text from PDF pages...');
        await new Promise(resolve => setTimeout(resolve, 1000));

        setProcessingStatus('Summarizing content...');
        await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        setProcessingStatus('Extracting text from image...');
        await new Promise(resolve => setTimeout(resolve, 1000));

        setProcessingStatus('Summarizing content...');
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      setProcessingStatus('Analyzing content type...');
      await new Promise(resolve => setTimeout(resolve, 1000));

      setProcessingStatus('Generating intelligent animation...');
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Step 3: Process file
      console.log('Processing file with ID:', fileId);
      const processResponse = await fetch(`http://localhost:8080/api/text-to-animation/process/${fileId}`, {
        method: 'POST',
      });
      console.log('Process response:', processResponse);

      if (!processResponse.ok) {
        throw new Error('Processing failed');
      }

      const processData = await processResponse.json();
      console.log('Process data:', processData);
      const videoUrl = processData.download_url;
      console.log('Generated video URL:', videoUrl);

      setProcessingStatus('Video generated successfully!');
      setGeneratedVideo(videoUrl);

    } catch (error) {
      console.error('Error in processTextToAnimation:', error);
      setProcessingStatus('Error: ' + error.message);
    } finally {
      setIsProcessing(false);
    }
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
        <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
          <div />
          <UserBadge />
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
          <button
            className={`toggle-btn ${uploadMode === 'text-to-animation' ? 'active' : ''}`}
            onClick={() => setUploadMode('text-to-animation')}
          >
            Text to Animation
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

        {/* Text-to-Animation Upload Area */}
        {uploadMode === 'text-to-animation' && (
          <div className="text-to-animation-area">
            <div className="text-to-animation-info">
              <h3>🎬 Text to Animation</h3>
              <p>Upload your handwritten notes, typed documents, or PDFs and we'll convert them into engaging animated videos!</p>
              <div className="supported-formats">
                <p><strong>Supported formats:</strong> PDF, PNG, JPG, JPEG</p>
              </div>
            </div>

            {/* File Preview Section */}
            {uploadedFilePreview && (
              <div className="file-preview-section">
                <h4>📋 Uploaded File Preview</h4>
                <div className="file-preview-container">
                  {uploadedFilePreview === 'pdf' ? (
                    <div className="pdf-preview">
                      <div className="pdf-icon">📄</div>
                      <p className="pdf-filename">{selectedFiles[0]?.name}</p>
                      <p className="pdf-info">PDF Document</p>
                    </div>
                  ) : (
                    <div className="image-preview">
                      <img
                        src={uploadedFilePreview}
                        alt="Uploaded preview"
                        className="preview-image"
                      />
                      <p className="image-info">{selectedFiles[0]?.name}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            <div
              className="animation-drop-zone"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              <div className="animation-upload-icon">📄</div>
              <h3>Drop your notes or documents here</h3>
              <p>Upload handwritten notes, typed documents, or PDFs</p>
              <input
                type="file"
                multiple
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={handleFileSelect}
                className="file-input"
                id="animation-file-input"
              />
              <label htmlFor="animation-file-input" className="choose-files-btn">
                Choose Files
              </label>
            </div>

            {/* Processing Status */}
            {isProcessing && (
              <div className="processing-status">
                <div className="processing-spinner"></div>
                <p>{processingStatus}</p>
              </div>
            )}

            {/* Generated Video Preview */}
            {generatedVideo && (
              <div className="video-preview">
                <h3>Generated Video</h3>
                <video controls width="100%" src={generatedVideo} />
                <div className="video-actions">
                  <button className="download-btn" onClick={() => window.open(generatedVideo, '_blank')}>
                    Download Video
                  </button>
                  <button className="save-btn">
                    Save to Library
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Submit Button */}
        <button className="submit-btn" onClick={handleSubmit}>Let's Make Something Cool!</button>
      </div>
    </div>
  );
};

export default VideosPage;
