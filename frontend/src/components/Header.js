import React from 'react';

const Header = ({ datasetName, onReset, onDownload, showActions }) => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="header" data-testid="header">
      <div className="header-content">
        <a href="/" className="logo" data-testid="app-logo">
          <img src="/logo.png" alt="DataForge" className="logo-image" />
          <span className="logo-text">DataForge</span>
        </a>
        
        {/* Navigation Links */}
        {!showActions && (
          <nav className="nav-links" data-testid="nav-links">
            <button className="nav-link" onClick={() => scrollToSection('hero')} data-testid="nav-home">
              Home
            </button>
            <button className="nav-link" onClick={() => scrollToSection('features')} data-testid="nav-features">
              Features
            </button>
            <button className="nav-link" onClick={() => scrollToSection('about')} data-testid="nav-about">
              About
            </button>
            <button className="nav-link" onClick={() => scrollToSection('how-it-works')} data-testid="nav-process">
              Process
            </button>
          </nav>
        )}
        
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
