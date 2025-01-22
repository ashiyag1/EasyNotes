// src/components/Navbar.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user'));

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <nav className="navbar">
      <h1>EasyNotes</h1>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        {user ? (
          <>
            <li>
              <Link to="/notes">My Notes</Link>
            </li>
            <li>
              <Link to="/public">Public Notes</Link>
            </li>
            <li onClick={handleLogout} className="logout-button">
              Logout
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/public">Public Notes</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
