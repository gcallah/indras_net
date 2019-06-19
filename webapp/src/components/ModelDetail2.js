import React, { Component } from "react";
import { Loader, Card, Dimmer } from "semantic-ui-react";
import axios from 'axios';

class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/';

  state = {
    msg: '',
    model_detail: {},
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Title";
    const res = await axios.get(this.api_server + 'models/' + this.props.id)
    this.setState({ model_detail: res.data });

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

    return (
      <div>
        <br />
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!</h1>
        <br /><br />

        <Card key={id} fluid style={{ overflowWrap: 'break-word' }}>
          <Card.Content>
            <Card.Header>Model Name: {this.state.model_detail.name}</Card.Header>
            <Card.Meta>Description: {this.state.model_detail.description}</Card.Meta>
          </Card.Content>
        </Card>

        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;