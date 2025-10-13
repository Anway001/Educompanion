import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Sidebar.css';

const Sidebar = ({ show }) => {
  return (
    <div className={`sidebar ${show ? 'show' : ''}`}>
      <div className="sidebar-header">
        <div className="brand">EduCompanion</div>
      </div>
      <div className="sidebar-search">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="search-icon" viewBox="0 0 16 16">
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
        </svg>
        <input type="text" placeholder="Search" />
      </div>
      <nav className="sidebar-nav">
        <ul>
          <li><Link to="/">Ask EduCompanion</Link></li>
          <li><Link to="/explore">Explore</Link></li>
          <li><Link to="/visuals">Visuals</Link></li>
        </ul>
      </nav>
      <div className="sidebar-recents">
        <p>Recents</p>
        <ul>
          <li><a href="#generate-instagram">Generate Instagram Capti...</a></li>
          <li><a href="#create-uiux">Create UI/UX Copy for Mo...</a></li>
          <li><a href="#craft-engaging">Craft Engaging Facebook...</a></li>
          <li><a href="#write-blog">Write Blog Post on Remot...</a></li>
          <li><a href="#design-social">Design Social Media Strat...</a></li>
          <li><a href="#develop-landing">Develop Landing Page Co...</a></li>
        </ul>
      </div>
      <div className="sidebar-last-week">
        <p>Last Week</p>
        <ul>
            <li><a href="#generate-email">Generate Email Campaig...</a></li>
            <li><a href="#create-customer">Create Customer Feedba...</a></li>
            <li><a href="#draft-linkedin">Draft Linkedin Post for Bu...</a></li>
            <li><a href="#write-marketing">Write Marketing Plan for...</a></li>
            <li><a href="#generate-faq">Generate FAQ Section for...</a></li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
