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
      model_detail: {},
      loadingData: false,
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Property";
    const {menu_id} = this.props.location.state
    const res = await axios.get(this.api_server + menu_id.id)
    this.setState({ model_detail: res.data });
    console.log(this.state.model_detail)
    this.states(res.data);
    this.setState({ loadingData: false });
  }
  
  states(data){
    //loop over objects in data and create object in this.state
    Object.keys(this.state.model_detail).forEach(item => 
         this.setState({[item]: data[item]})
                                       );
  }

 renderData(data){
  Object.keys(this.state).forEach(item => console.log(1))}


  handleChange = (event) => {
   //this.setState({ [target['val']]: target.value });
   let newVar = JSON.parse(JSON.stringify(this.state[event.target.name]))
   //make changes to ingredients
    newVar['val'] = event.target.value 
    this.setState({
      [event.target.name] : newVar
    }) 
   console.log(this.state[event.target.name])
  }

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
            {this.state.grid_height ?<label> {this.state.grid_height['question']} : <input type="int" defaultValue={this.state.grid_height['val']} onChange={this.handleChange} minValue ={this.state.grid_height['loval']} maxValue={this.state.grid_height['hival']} name='grid_height' /><br /><br /></label>: null}
            {this.state.grid_width ? <label> {this.state.grid_width['question']} : <input type="int" defaultValue={this.state.grid_width['val']} name='grid_width' minValue ={this.state.grid_width['loval']} maxValue={this.state.grid_width['hival']} onChange={this.handleChange}/> <br /><br/></label> : null}

         {this.state.num_blue ? <label> {this.state.num_blue['question']} : <input type="int"      defaultValue={this.state.num_blue['val']} onChange={this.handleChange} minValue ={this.state.num_blue['loval']} maxValue={this.state.num_blue['hival']} name='num_blue' /><br /><br /></label>: null}
         {this.state.num_red ? <label> {this.state.num_red['question']} : <input type="int"      defaultValue={this.state.num_red['val']} minValue ={this.state.num_red['loval']} maxValue={this.state.num_red['hival']}  onChange={this.handleChange} name='num_red' /></label>: null}
        </form>
        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;
