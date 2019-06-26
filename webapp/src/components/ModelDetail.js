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
      },
     console.log(this.state.model_details))
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
            {
           Object.keys(this.state.model_details).map((item,i)=> {
                return(<label key={i}>{this.state.model_details[item]['question']} :<input type={this.state.model_details[item]['atype']} defaultValue={this.state.model_details[item]['val']} onChange={this.handleChange} name={item} /><br/><br/></label>
            )})
        }
        </form>
        <br /><br />
        <button onClick={this.handleSubmit}>Submit</button>
      </div>
    );
  }
}

export default ModelDetail;
