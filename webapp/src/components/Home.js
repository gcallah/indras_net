import React, { Component } from "react";
import { Loader, Dimmer, Menu } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

var image = require('./images/model_images.png')

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
          <Link to={{
                pathname: `/models/props/${id}`, 
                state:{ menu_id:id, name:item.name}
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

        <h1 style={{"fontSize": 16}}>We have several models: </h1>
        {this.state.allItems && this.renderMenu()}
        <img alt="" style={{display:'block', marginLeft:'auto', marginRight:'auto', width:'50%'}} src={image} align="middle"/>
        <br /><br />
      </div>
    );
  }
}

export default Home;
