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

  showSource = () => {
    window.open('https://gcallah.github.io/indras_net/index.html')
  }

  handleClick(id, name, source){
    localStorage.setItem("menu_id", id)
    localStorage.setItem("name", name)
    localStorage.setItem("source", source)
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
        <h1 style={{ "textAlign": "center", "fontWeight": '200'}}>Welcome to the Indra ABM platform!</h1>
        <br /><br />
        <h1 style={{"fontSize": 16, "fontWeight": '400'}}>We have several models: </h1>
        <img alt="" style={{display:'block', float:'right', width:'40%', alignItems: "center"}} src={model_image}/>
        <Menu vertical style={{
            maxHeight: '30em',
            maxwidth: '40em',
            overflowY: 'scroll',
          }}>
        {Object.keys(this.state.allItems).map((item,i)=>
        <Menu.Item key={i}>
          {console.log(this.state.allItems[item]['model ID'])}
          <Link to="/models/props/" onClick={() => this.handleClick(this.state.allItems[item]['model ID'], this.state.allItems[item]['name'], this.state.allItems[item]['source'])}>
            {this.state.allItems[item]['name']}
          </Link>
        </Menu.Item>)}
        </Menu>
        <h1 style={{"fontSize": 16, "fontWeight": '400'}}>To see the
        <button onClick={this.showSource}
        className="btn btn-outline-primary m-2"> description </button> 
        of the project.</h1>
        <br /><br />
        <br /><br />
      </div>
    );
  }
}

export default Home;
