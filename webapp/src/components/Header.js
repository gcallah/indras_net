import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <div className="header">
      <Link to="/">
        <div className="indra-name">
          <p>Indra</p>
        </div>
      </Link>
    </div>
  );
}

export default Header;
