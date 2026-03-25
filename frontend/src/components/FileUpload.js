import React, { useRef } from 'react';
import { Upload } from 'lucide-react';

const FileUpload = ({ onFileSelect, loading }) => {
  const inputRef = useRef(null);

  const handleClick = () => {
    inputRef.current.click();
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const maxSize = 500 * 1024 * 1024; // 500MB
      if (file.size > maxSize) {
        alert(`File too large! Max size: 500MB (current: ${(file.size / 1024 / 1024).toFixed(1)}MB)`);
        return;
      }
      onFileSelect(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.currentTarget.style.borderColor = '#D90429';
    e.currentTarget.style.background = 'white';
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.currentTarget.style.borderColor = '#cbd5e1';
    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.8)';
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.currentTarget.style.borderColor = '#cbd5e1';
    e.currentTarget.style.background = 'rgba(255, 255, 255, 0.8)';
    const file = e.dataTransfer.files[0];
    if (file) {
      const maxSize = 500 * 1024 * 1024;
      if (file.size > maxSize) {
        alert(`File too large! Max size: 500MB (current: ${(file.size / 1024 / 1024).toFixed(1)}MB)`);
        return;
      }
      onFileSelect(file);
    }
  };

  return (
    <div 
      className="upload-zone" 
      onClick={handleClick}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      data-testid="upload-zone"
    >
      {/* Branding Text */}
      <div className="upload-branding">
        <div className="upload-branding-title" data-testid="upload-title">DATA FORGE</div>
        <div className="upload-branding-subtitle" data-testid="upload-subtitle">YOUR DATA, PERFECTED.</div>
      </div>

      {/* Upload Icon */}
      <div className="upload-icon">
        <Upload />
      </div>
      
      <h3>Drag & Drop Your Dataset</h3>
      <p>Supports CSV and Excel files <strong>(up to 500MB)</strong></p>
      
      <input 
        type="file" 
        ref={inputRef} 
        style={{ display: 'none' }} 
        onChange={handleChange} 
        accept=".csv, .xlsx"
        data-testid="file-input"
      />

      <button 
        className="btn btn-primary" 
        disabled={loading}
        data-testid="upload-button"
      >
        {loading ? 'Uploading...' : 'Select File'}
      </button>
    </div>
  );
};

export default FileUpload;
