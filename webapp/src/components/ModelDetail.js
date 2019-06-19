import React, { Component } from "react";
import { Loader, Card, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/props/';
  state = {
    msg: '',
    model_detail: {},
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Property";
    console.log("This is props.id: ")
    const {menu_id} = this.props.location.state
    const res = await axios.get(this.api_server + menu_id.id)
    console.log(res.data)
    this.setState({ model_detail: res.data });
    this.setState({ loadingData: false });
  }

  renderModelDetail= () => {
      return (
        <div>
          <Card key={this.props.id}>
            <Link to={{
              pathname: `/models/props/` + this.props.location.state.id,
              state: {
                msg: 'Linking the ModelDetail',
                model_detail: this.state.model_detail
              }
            }}>
            </Link>
          </Card>
        </div>
      );
    return <Card.Content>{this.state.model_detail}</Card.Content>;
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
        <h1 style={{ "textAlign": "center" }}> List of properties </h1>
        <br /><br />
        {this.state.model_detail && this.renderModelDetail()}
        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;