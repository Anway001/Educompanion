import React from 'react';

const EduCompanionLogo = ({ width = 40, height = 40, className }) => {
  return (
    <svg 
      width={width} 
      height={height} 
      viewBox="0 0 40 40" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#00b894" />
          <stop offset="100%" stopColor="#0984e3" />
        </linearGradient>
      </defs>
      
      {/* Main circle background */}
      <circle cx="20" cy="20" r="18" fill="url(#logoGradient)" />
      
      {/* Book/Education symbol */}
      <path 
        d="M12 10 L28 10 L28 30 L20 26 L12 30 Z" 
        fill="white"
      />
      
      {/* Book pages lines */}
      <line x1="15" y1="14" x2="25" y2="14" stroke="#00b894" />
      <line x1="15" y1="17" x2="25" y2="17" stroke="#00b894" />
      <line x1="15" y1="20" x2="22" y2="20" stroke="#00b894" />
      
      {/* Companion/AI symbol */}
      <circle cx="24" cy="12" r="2" fill="#0984e3" />
      <circle cx="25" cy="11" r="1" fill="white" opacity="0.8" />
    </svg>
  );
};

export default EduCompanionLogo;
