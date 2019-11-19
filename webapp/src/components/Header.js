import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <div className="header">
      <div className="indra-name">
        <Link to="/">
          <p>INDRA</p>
        </Link>
      </div>
    </div>
  );
}

export default Header;
