import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import EduCompanionLogo from './EduCompanionLogo';
import '../styles/LoginPage.css';

const LoginPage = ({ onLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  setIsLoading(true);

  try {
    const response = await axios.post("http://localhost:8080/api/auth/login", formData);

    // adjust keys based on your backend response
    const { access_token, user } = response.data;

    localStorage.setItem("access_token", access_token);
    localStorage.setItem("user", JSON.stringify(user));

    console.log("Login successful:", user);
    onLogin(); // callback after successful login
  } catch (error) {
    console.error("Login error:", error.response?.data || error.message);
    alert(error.response?.data?.message || "Invalid email or password");
  } finally {
    setIsLoading(false);
  }
};


  return (
    <div className="login-page">
      <div className="floating-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
        <div className="shape shape-4"></div>
      </div>
      
      <div className="login-container">
        <div className="logo-section">
          <EduCompanionLogo width={60} height={60} className="login-logo" />
          <h1 className="brand-title">EduCompanion</h1>
          <p className="brand-subtitle">Your AI Learning Partner</p>
        </div>
        
        <div className="form-section">
          <h2>Welcome Back</h2>
          <p className="form-description">Sign in to continue your learning journey</p>
          
          <form onSubmit={handleSubmit} className="login-form">
            <div className="input-group">
              <input 
                type="email" 
                name="email"
                placeholder="Email Address" 
                value={formData.email}
                onChange={handleChange}
                required 
                className="form-input"
              />
              <span className="input-highlight"></span>
            </div>
            
            <div className="input-group">
              <input 
                type="password" 
                name="password"
                placeholder="Password" 
                value={formData.password}
                onChange={handleChange}
                required 
                className="form-input"
              />
              <span className="input-highlight"></span>
            </div>
            
            <button 
              type="submit" 
              className={`login-btn ${isLoading ? 'loading' : ''}`}
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="loading-spinner"></span>
              ) : (
                'Sign In'
              )}
            </button>
          </form>
          
          <div className="form-footer">
            <p>
              Don't have an account? 
              <Link to="/signup" className="signup-link">Create Account</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
