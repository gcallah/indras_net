import React from 'react';
import Card from 'react-bootstrap/Card';
import propTypes from 'prop-types';

const CardWrapper = ({ title, children }) => (
  <Card>
    <Card.Header>{title}</Card.Header>
    <Card.Body>{children}</Card.Body>
  </Card>
);

CardWrapper.propTypes = {
  title: propTypes.string.isRequired,
  children: propTypes.node.isRequired,
};

export default CardWrapper;
