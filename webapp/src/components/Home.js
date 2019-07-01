import React, { Component } from "react";
import { Loader, Dimmer, Menu } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

class Home extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/';
  state = {
    msg: '',
    allItems: [],
    loadingData: false,
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      document.title = "Indra | Home";
      const res = await axios.get(this.api_server + 'models')
      this.setState({ allItems: res.data });
      this.setState({ loadingData: false });
    } catch (e) {
      console.log(e.message);
    } 
  }

  renderMenu = () => {
    let items = this.state.allItems.map((item, id) => {
      return (
        <Menu.Item key={id} >
          <Link 
              to={{
                pathname: '/models/props/'+id, 
                state:{ menu_id: {id}, name:item.name}
              }}>
          {item.name}</Link>
        </Menu.Item>
      );
    });

    return <Menu vertical style={{
      maxHeight: '30em',
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
