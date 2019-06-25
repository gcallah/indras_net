import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';


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
    const properties = await axios.get(this.api_server + menu_id.id);
    this.setState({ model_details: properties.data });
    this.states(properties.data);
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
    return (
      <div>
        <br />
        <br />
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!</h1>
        <h1 style={{ "textAlign": "left" }}> List of properties </h1>
        <br /><br />
        <form>
            {this.state.grid_height ?<label> {this.state.grid_height['question']} : <input type="int" placeholder={this.state.grid_height['val']} onChange={this.handleChange} name='grid_height' /><br /><br /></label>: null}
            {this.state.grid_width ? <label> {this.state.grid_width['question']} : <input type="int" placeholder={this.state.grid_width['val']} name='grid_width' onChange={this.handleChange}/> <br /><br/></label> : null}

         {this.state.num_blue ? <label> {this.state.num_blue['question']} : <input type="int"      placeholder={this.state.num_blue['val']} onChange={this.handleChange} name='num_blue' /><br /><br /></label>: null}
         {this.state.num_red ? <label> {this.state.num_red['question']} : <input type="int" placeholder={this.state.num_red['val']} onChange={this.handleChange} name='num_red' /><br /><br /></label>: null}
         {this.state.density ? <label> {this.state.density['question']} : <input type="float" placeholder={this.state.density['val']} onChange={this.handleChange} name='density' /><br /><br /></label>: null}
         {this.state.density ? <label> {this.state.density['question']} : <input type="float" placeholder={this.state.density['val']} onChange={this.handleChange} name='density' /><br /><br /></label>: null}
        </form>
        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;
