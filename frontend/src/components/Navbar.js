import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../utils/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🏥 Health Monitor
        </Link>
        {user && (
          <ul className="navbar-menu">
            <li><Link to="/">Dashboard</Link></li>
            <li><Link to="/metrics">Metrics</Link></li>
            <li><Link to="/predictions">Predictions</Link></li>
            <li><Link to="/tips">Health Tips</Link></li>
            <li className="navbar-user">
              <span>👤 {user.username}</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </li>
          </ul>
        )}
      </div>
    </nav>
  );
};

export default Navbar;