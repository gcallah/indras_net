import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';

class Menu extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/menu/';
  state = {
    msg: '',
    menu_list:{},
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Menu";
    const menu = await axios.get(this.api_server);
    this.setState({menu_list:menu.data})
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
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!
        </h1>
        <br /><br />
          { Object.keys(this.state.menu_list).map((item,i)=>
     <li key={i}>{this.state.menu_list[item]['question']}</li>)}
        
        <br /><br />
      </div>
    );
  }
}

export default Menu;
