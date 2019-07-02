import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";

class Action extends Component {
  state = {
    msg: '',
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Action";
    const {menu_id} = this.props.location.state;
    this.setState({ loadingData: false });
  }

  render() {
    if (this.state.loadingData) {
    return (
    <Dimmer active inverted>
    <Loader size='massive'>Loading...</Loader>
    </Dimmer>
    );
  }

  var imageName = require('./images/forestfire.png')

  return (
    <div>
      <br />
      <h2 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!
      </h2>
      <br /><br />
      
      <p>We are updating the model! The figure like this will be displayed soon!</p>
      <img src={imageName} />

      <br /><br />
    </div>
    );
  }
}

export default Action;
