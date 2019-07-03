import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";

class ScatterPlot extends Component {
  state = {
    msg: '',
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Action";
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
    let imageName = require('./images/forestfire.png')
    return (
      <div>
        <br />
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!
        </h1>
        <br /><br />

        <p>We are updating the model! The figure like this will be displayed soon!</p>
      <img src={imageName} />

        <br /><br />
      </div>
    );
  }
}

export default ScatterPlot;
