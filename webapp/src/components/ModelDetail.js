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
    this.setState({id:menu_id.id})
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

 handleChange = (e) =>{ 
   let model_detail = this.state.model_details;
   const {name,value} = e.target
   model_detail[name]['val']= value
   this.setState({model_details:model_detail}) 
}
  handleSubmit = event => {
    event.preventDefault();
    axios.put(this.api_server + this.state.id,this.state.model_details)
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
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
            {this.state.grid_height ?<label> {this.state.grid_height['question']} : <input type="int" defaultValue={this.state.grid_height['val']} onChange={this.handleChange} name='grid_height' /><br /><br /></label>: null}
            {this.state.grid_width ? <label> {this.state.grid_width['question']} : <input type="int" defaultValue={this.state.grid_width['val']} name='grid_width' onChange={this.handleChange}/> <br /><br/></label> : null}

         {this.state.num_blue ? <label> {this.state.num_blue['question']} : <input type="int"      defaultValue={this.state.num_blue['val']} onChange={this.handleChange} name='num_blue' /><br /><br /></label>: null}
         {this.state.num_red ? <label> {this.state.num_red['question']} : <input type="int" defaultValue={this.state.num_red['val']} onChange={this.handleChange} name='num_red' /><br /><br /></label>: null}
         {this.state.density ? <label> {this.state.density['question']} : <input type="float" defaultValue={this.state.density['val']} onChange={this.handleChange} name='density' /><br /><br /></label>: null}
         {this.state.mean_tol ? <label> {this.state.mean_tol['question']} : <input type="float" defaultValue={this.state.mean_tol['val']} onChange={this.handleChange} name='mean_tol' /><br /><br /></label>: null}
         {this.state.tol_deviation ? <label> {this.state.tol_deviation['question']} : <input type="float" defaultValue={this.state.tol_deviation['val']} onChange={this.handleChange} name='tol_deviation' /><br /><br /></label>: null}
         {this.state.num_sheep ? <label> {this.state.num_sheep['question']} : <input type="int" defaultValue={this.state.num_sheep['val']} onChange={this.handleChange} name='num_sheep' /><br /><br /></label>: null}
         {this.state.num_wolves ? <label> {this.state.num_wolves['question']} : <input type="int" defaultValue={this.state.num_wolves['val']} onChange={this.handleChange} name='num_wolves' /><br /><br /></label>: null}
         {this.state.num_consumers ? <label> {this.state.num_consumers['question']} : <input type="int" defaultValue={this.state.num_consumers['val']} onChange={this.handleChange} name='num_consumers' /><br /><br /></label>: null}
         {this.state.num_producers ? <label> {this.state.num_producers['question']} : <input type="int" defaultValue={this.state.num_producers['val']} onChange={this.handleChange} name='num_producers' /><br /><br /></label>: null}
        </form>
        <br /><br />
        <button onClick={this.handleSubmit}>Submit</button>
      </div>
    );
  }
}

export default ModelDetail;
