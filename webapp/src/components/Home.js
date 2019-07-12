import React, { Component } from "react";
import { Loader, Dimmer, Menu } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

var model_image = require('./images/model_images.png')

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
      console.log(this.state.allItems)
    } catch (e) {
      console.log(e.message);
    } 
  }


  handleClick(id, name){
    console.log(id)
    localStorage.setItem("menu_id", id)
    localStorage.setItem("name", name)
    console.log(localStorage.getItem("menu_id"))
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
        <Menu vertical style={{
            maxHeight: '30em',
            maxwidth: '40em',
            overflowY: 'scroll',
          }}>

        {Object.keys(this.state.allItems).map((item,i)=>
        <Menu.Item key={i}>
          {console.log(this.state.allItems[item]['model ID'])}
          <Link to="/models/props/" onClick={() => this.handleClick(this.state.allItems[item]['model ID'], this.state.allItems[item]['name'])}>
            {this.state.allItems[item]['name']}
          </Link>
        </Menu.Item>)}
        </Menu>
        <br /><br />
        <img alt="" style={{display:'block', marginLeft:'auto', marginRight:'auto', width:'50%'}} src={model_image} align="middle"/>
        <br /><br />
      </div>
    );
  }
}

export default Home;
