import React, { Component } from "react";
import { Loader, Dimmer, Menu } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';
import ModelMenu from "./ModelMenu"

var model_image = require('./images/model_images.png')
var sandpile_img = require('./images/Sandpile.jpg')

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
      const doc = localStorage.getItem("doc");
      this.setState({doc:doc});
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
        <h1 style={{ "textAlign": "center", "fontWeight": '200'}}>Indra Agent-Based Modeling System</h1>
        <br /><br />
        <h1 style={{"fontSize": 16, "fontWeight": '400'}}>Please choose a model: </h1>
        <img src={sandpile_img} class="rounded-circle" alt="Responsive image" style={{display:'block', float:'right', width:'45%', alignItems: "center"}} data-toggle="tooltip" data-placement="top" title="Image by Seth Terashima."/>
        <ul class="list-group">
          <div class="row">
            <div class="col">
        {Object.keys(this.state.allItems).map((item,i)=>
        <a class=" w-50 p-3 list-group-item list-group-item-action"  key={i}>
          {console.log(this.state.allItems[item]['model ID'])}
          <Link to= {{pathname: `/models/props/${i}`}}
            class="text-primary" data-toggle="tooltip"  data-placement="top" title={this.state.allItems[item]['doc']}  onClick={() => this.handleClick(this.state.allItems[item]['model ID'], this.state.allItems[item]['name'], this.state.allItems[item]['source'])}>
            {this.state.allItems[item]['name']}
          </Link>
        </a>)}
        </div></div> </ul>
        <h1 style={{"fontSize": 16, "fontWeight": '400'}}>
        <a href="#" class="text-primary m-2" onClick={this.showSource}>
        View Project Description </a> </h1>
        <br /><br />
        <br /><br />
      </div>
    );
  }
}

export default Home;
