/* eslint-disable react/prop-types */
/* eslint-disable react/destructuring-assignment */
/* eslint no-trailing-spaces: "error" */
import React from 'react';
import { Link, HashRouter as Router } from 'react-router-dom';
import { Button } from 'react-bootstrap';

const BackHomeButton = () => (
  <Router>
    <Link to="/">
      <Button variant="primary">Back Home</Button>
    </Link>
  </Router>
);

export default BackHomeButton;
