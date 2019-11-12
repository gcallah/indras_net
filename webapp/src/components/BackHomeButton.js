/* eslint-disable react/prop-types */
/* eslint-disable react/destructuring-assignment */
/* eslint no-trailing-spaces: "error" */
import React from 'react';
import autoBind from 'react-autobind';
import { Redirect } from 'react-router-dom';
import { Button } from 'react-bootstrap';

export default class BackHomeButton extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.state = {
      clicked: false,
    };
  }

  handleClick() {
    this.setState({ clicked: true });
  }

  render() {
    if (this.state.clicked) {
      return <Redirect to="/" />;
    }
    return (
      <Button variant="primary" onClick={this.handleClick}>Back Home</Button>
    );
  }
}
