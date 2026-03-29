import React from 'react';

const Footer = () => {
  return (
    <footer className="footer" data-testid="footer">
      <div className="footer-simple">
        <div className="footer-brand">
          <div className="footer-logo">
            <img src="/logo.png" alt="DataForge" className="footer-logo-image" />
            <span className="footer-logo-text">DataForge</span>
          </div>
          <p className="footer-tagline">
            Your Data, Perfected. Transform messy data into crystal clear insights.
          </p>
        </div>
        
        <div className="footer-bottom">
          <p className="footer-copyright">
            © {new Date().getFullYear()} DataForge. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
