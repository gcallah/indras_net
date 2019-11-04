import React from 'react';
import { Menu } from 'semantic-ui-react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <div>
      <Menu.Item><Link to="/" /></Menu.Item>
      <Menu.Menu position="right">
        <Menu.Item>
          <Link to="/" />
        </Menu.Item>
      </Menu.Menu>
    </div>
  );
}

export default Header;
