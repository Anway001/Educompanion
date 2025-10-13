import React from 'react';
import '../styles/UserBadge.css';

const UserBadge = () => {
  let name = '';
  try {
    const stored = localStorage.getItem('user');
    if (stored) {
      const u = JSON.parse(stored);
      name = `${u.first_name || ''}${u.last_name ? ' ' + u.last_name : ''}`.trim();
    }
  } catch (e) {
    // ignore
  }

  if (!name) return null;

  return (
    <div className="user-badge">
      <div className="user-avatar">{(name[0] || '').toUpperCase()}</div>
      <div className="user-name">{name}</div>
    </div>
  );
};

export default UserBadge;
