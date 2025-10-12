import React, { useState } from 'react';
import { Link , useNavigate} from 'react-router-dom';
import axios from 'axios';
import EduCompanionLogo from './EduCompanionLogo';
import '../styles/SignupPage.css';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: ''
  });
  const navigate = useNavigate();
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
      const response = await axios.post("http://localhost:8080/api/auth/signup", formData);

      console.log("Signup successful:", response.data);
      navigate('/login');
    } catch (error) {
      console.error("Signup error:", error.response?.data || error.message);
      alert(error.response?.data?.message || "Signup failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signup-page">
      <div className="floating-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
        <div className="shape shape-4"></div>
      </div>
      
      <div className="signup-container">
        <div className="logo-section">
          <EduCompanionLogo width={60} height={60} className="signup-logo" />
          <h1 className="brand-title">EduCompanion</h1>
          <p className="brand-subtitle">Your AI Learning Partner</p>
        </div>
        
        <div className="form-section">
          <h2>Join EduCompanion</h2>
          <p className="form-description">Start your personalized learning experience</p>
          
          <form onSubmit={handleSubmit} className="signup-form">
            {/* First Name */}
            <div className="input-group">
              <input 
                type="text" 
                name="first_name"
                placeholder="First Name" 
                value={formData.first_name}
                onChange={handleChange}
                required 
                className="form-input"
              />
              <span className="input-highlight"></span>
            </div>

            {/* Last Name */}
            <div className="input-group">
              <input 
                type="text" 
                name="last_name"
                placeholder="Last Name" 
                value={formData.last_name}
                onChange={handleChange}
                required 
                className="form-input"
              />
              <span className="input-highlight"></span>
            </div>
            
            {/* Email */}
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
            
            {/* Password */}
            <div className="input-group">
              <input 
                type="password" 
                name="password"
                placeholder="Create Password" 
                value={formData.password}
                onChange={handleChange}
                required 
                className="form-input"
              />
              <span className="input-highlight"></span>
            </div>
            
            <div className="terms-text">
              By signing up, you agree to our{' '}
              <a href="#" className="terms-link">Terms of Service</a>{' '}
              and{' '}
              <a href="#" className="terms-link">Privacy Policy</a>.
            </div>
            
            <button 
              type="submit" 
              className={`signup-btn ${isLoading ? 'loading' : ''}`}
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="loading-spinner"></span>
              ) : (
                'Create Account'
              )}
            </button>
          </form>
          
          <div className="form-footer">
            <p>
              Already have an account? 
              <Link to="/login" className="login-link">Sign In</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
