import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';

class Run extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loadingData: false,
    };
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = 'Indra | Action';
    this.setState({ loadingData: false });
  }

  render() {
    const { loadingData } = this.state;
    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading...</Loader>
        </Dimmer>
      );
    }

    return (
      <div>
        <br />
        <h1 style={{ textAlign: 'center' }}>
          Welcome to the Indra ABM platform!
        </h1>
        <br />
        <br />
        <p>We will have this model running soon!</p>
        <br />
        <br />
      </div>
    );
  }
}

export default Run;
