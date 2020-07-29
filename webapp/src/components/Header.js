import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const home = '/';

function Header() {
  return (
    <Navbar bg="light" expand="lg">
      <Nav className="mr-auto">
        <Nav.Link as={Link} to={home}>
          HOME
        </Nav.Link>
      </Nav>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link
            href="https://gcallah.github.io/indras_net/index.html"
          >
            ABOUT
          </Nav.Link>
          <Nav.Link href="https://github.com/gcallah/indras_net/">
            SOURCE CODE
          </Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default Header;
