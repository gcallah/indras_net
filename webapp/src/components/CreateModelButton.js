import React from 'react';
import { Link, HashRouter as Router } from 'react-router-dom';
import { Button } from 'react-bootstrap';

const CreateModelButton = () => (
  <Router>
    <Link to="modelcreator">
      <Button variant="outline-primary">Create a new model</Button>
    </Link>
  </Router>
);

export default CreateModelButton;
