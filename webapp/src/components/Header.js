import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <div className="header">
      <ul className="header-items-list">
        <li className="header-item indra-name">
          <Link to="/">
            <p>INDRA</p>
          </Link>
        </li>
        <li className="header-item">
          <a href="https://gcallah.github.io/indras_net/index.html" target="_blank" rel="noopener noreferrer">
            <p>ABOUT</p>
          </a>
        </li>
        <li className="header-item">
          <a href="https://github.com/gcallah/indras_net/" target="_blank" rel="noopener noreferrer">
            <p>SOURCE CODE</p>
          </a>
        </li>
      </ul>
    </div>
  );
}

export default Header;
