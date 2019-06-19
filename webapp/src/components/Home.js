import React, { Component } from "react";
import { Loader, Dimmer, Menu, Card, CardHeader } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';
import ModelDetail from './ModelDetail';

class Home extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/';
  state = {
    msg: '',
    allItems: [],
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Title";
    const res = await axios.get(this.api_server + 'models')
    this.setState({ allItems: res.data });
    this.setState({ loadingData: false });
  }


  renderMenu = () => {
    console.log("DEBUGGING")
    let items = this.state.allItems.map((item, id) => {
      console.log("This is in renderMenu: ")
      console.log(id)
      console.log(item.name)
      if (this.state.allItems && this.state.allItems.length) {
        console.log("It's not empty")
      }
      return (
        <div>
          <Card>
            <Card.Header key={id} href={'/models/props/' + id}> <Link to='/modelDetail'> </Link> {item.name}</Card.Header>
            <ModelDetail id={id} />
          </Card>
        </div>
      );
    });
    return <Menu vertical style={{
      maxHeight: '20em',
      maxwidth: '40em',
      overflowY: 'scroll',
    }}>{items}</Menu>;
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

        We have several models:
        {this.state.allItems && this.renderMenu()}
        <br /><br />
      </div>
    );
  }
}

export default Home;