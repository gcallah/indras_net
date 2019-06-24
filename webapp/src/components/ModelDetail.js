import 'rc-slider/assets/index.css';
import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';
import Slider from 'rc-slider'


class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/props/';
  constructor(props) {
    super(props);
    this.state = {
      msg: '',
      model_details: {},
      loadingData: false,
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Property";
    const {menu_id} = this.props.location.state;
    const res = await axios.get(this.api_server + menu_id.id);
    this.setState({ model_details: res.data });
    this.states(res.data);
    console.log(this.state.grid_height['hival']);
    this.setState({ loadingData: false });
  }
  
  states(data){
    //loop over objects in data and create object in this.state
    Object.keys(this.state.model_details).forEach(item => 
         this.setState({[item]: data[item]})
                                       );
  }

 renderData(data){
  Object.keys(this.state).forEach(item => console.log(1))}


handleChange = name => (e) => {
    let newVar = JSON.parse(JSON.stringify(this.state[name]))
    newVar['val'] = e
    this.setState({
      [name]: newVar 
    });
    let newVar1 = JSON.parse(JSON.stringify(this.state.model_details))
    newVar1[name]= this.state[name]
    this.setState({ model_details: newVar1 });
    console.log(this.state.model_details)
  };



  handleSubmit(event) {
    alert('grid_height: ' + this.state.grid_height);
    event.preventDefault();
  }

  render() {
    if (this.state.loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size='massive'>Loading...</Loader>
        </Dimmer>
      );
    }
    const inputStyle = { marginBottom: '10px', width:'3%'};
    return (
      <div>
        <br />
        <br />
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!</h1>
        <h1 style={{ "textAlign": "left" }}> List of properties </h1>
        <br /><br />
        <form>
            {this.state.grid_height ?<div><label>    {this.state.grid_height['question']}</label><input style={inputStyle} value={this.state.grid_height['val']}/><Slider style={{width:'50%'}}
          min={this.state.grid_height['lowval']}
          max={this.state.grid_height['hival']}
          defaultValue={this.state.grid_height['val']}
          onChange={this.handleChange('grid_height')}
        /><br /><br /></div>: null}
            
        </form>
        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;
