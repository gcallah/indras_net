import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function Header() {
  return (
    // <div className="header">
    //   <ul className="header-items-list">
    //     <li className="header-item indra-name">
    //       <Link to="/">
    //         <p>INDRA</p>
    //       </Link>
    //     </li>
    //     <li className="header-item">
    //       <a href="https://gcallah.github.io/indras_net/index.html" target="_blank" rel="noopener noreferrer">
    //         <p>ABOUT</p>
    //       </a>
    //     </li>
    //     <li className="header-item">
    //       <a href="https://github.com/gcallah/indras_net/" target="_blank" rel="noopener noreferrer">
    //         <p>SOURCE CODE</p>
    //       </a>
    //     </li>
    //   </ul>
    // </div>

    <Navbar bg="light" expand="lg">
      <Navbar.Brand href="/">INDRA</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href="https://gcallah.github.io/indras_net/index.html">ABOUT</Nav.Link>
          <Nav.Link href="https://github.com/gcallah/indras_net/">SOURCE CODE</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>

  );
}

export default Header;
