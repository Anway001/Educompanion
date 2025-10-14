import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import LoginPage from './components/LoginPage';
import SignupPage from './components/SignupPage';
import PodcastPage from './components/PodcastPage';
import NotesPage from './components/NotesPage';
import VideosPage from './components/VideosPage';
import VisualsPage from './components/VisualsPage';
import SettingsPage from './components/SettingsPage';
import ChatPage from './components/ChatPage';
import VerticalNavbar from './components/VerticalNavbar';
import SummarizerPage from './components/SummarizerPage';
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [sidebarVisible, setSidebarVisible] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleSignup = () => {
    setIsLoggedIn(true);
  };

  const toggleSidebar = () => {
    setSidebarVisible(!sidebarVisible);
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={isLoggedIn ? <Navigate to="/" /> : <LoginPage onLogin={handleLogin} />}
        />
        <Route
          path="/signup"
          element={isLoggedIn ? <Navigate to="/" /> : <SignupPage onSignup={handleSignup} />}
        />
        <Route
          path="/podcast"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <PodcastPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/summarize"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <SummarizerPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/chat"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <ChatPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/notes"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <NotesPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/videos"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <VideosPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/visuals"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <VisualsPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/settings"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <SettingsPage />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/*"
          element={
            isLoggedIn ? (
              <div className="app-layout">
                <VerticalNavbar onToggleSidebar={toggleSidebar} />
                <div className={`app ${sidebarVisible ? 'sidebar-open' : ''}`}>
                  <Sidebar show={sidebarVisible} />
                  <MainContent />
                </div>
              </div>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
