import React from 'react';

const Header = ({ datasetName, onReset, onDownload, showActions }) => {
  return (
    <header className="header" data-testid="header">
      <div className="header-content">
        <a href="/" className="logo" data-testid="app-logo">
          <img src="/logo.png" alt="DataForge" className="logo-image" />
          <span className="logo-text">DataForge</span>
        </a>
        
        {showActions && (
          <div className="header-actions">
            {datasetName && (
              <span className="dataset-name" data-testid="dataset-name">
                {datasetName}
              </span>
            )}
            
            <button 
              className="btn btn-success"
              onClick={onDownload}
              data-testid="download-button"
            >
              Download Clean Data
            </button>
            
            <button 
              className="btn btn-secondary"
              onClick={onReset}
              data-testid="reset-button"
            >
              Reset
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
