import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';

class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/props/';

  state = {
    model_details: {},
    loadingData: false,
    disabled_button: false,
  }


  async componentDidMount() {
    try{
      this.setState({ loadingData: true });
      document.title = "Indra | Property";
      const {menu_id} = this.props.location.state;
      const name = this.props.location.state.name;
      const properties = await axios.get(this.api_server + menu_id);
      this.setState({id:menu_id})
      this.setState({ model_details: properties.data });
      this.states(properties.data);
      this.errors(properties.data);
      this.setState({ loadingData: false });
      console.log(this.props.history.location)
    }catch(e){
      console.log(e.message);
    }
    
  }


  states = (data) => {
    //loop over objects in data and create object in this.state
    Object.keys(this.state.model_details).forEach(item => 
    this.setState({[item]: data[item]})
    );
  }


  errors = (data) => {
    Object.keys(this.state.model_details).forEach(item => 
      this.setState(prevState => ({
        model_details: {
          ...prevState.model_details,          
          [item]:{                     
          ...prevState.model_details[item],  
          errorMessage: '' ,
          disabledButton: false,       
          } 
        }
      })
    ))
  }


  errorSubmit = () =>{
    let ans = false
    Object.keys(this.state.model_details).forEach(item => 
    ans = ans || this.state.model_details[item]['disabledButton'])
    return ans
  }

  handleChange = (e) =>{ 
    let model_detail = this.state.model_details;
    const {name,value} = e.target
    let valid = this.checkValidity(name,value)

    if (valid === 1){
      model_detail[name]['val']= value
      model_detail[name]['errorMessage']=""
      model_detail[name]['disabledButton']=false
      this.setState({model_details:model_detail})

    } else if(valid === -1){
      model_detail[name]['errorMessage']="**Wrong Input Type"
      model_detail[name]['val']= this.state[name]['val']
      model_detail[name]['disabledButton']=true
      this.setState({model_details:model_detail})
      console.log(this.state.model_details[name])

    } else {
      model_detail[name]['errorMessage']=`**Please input a number between ${this.state[name]['lowval']} and ${this.state[name]['hival']}.`
      model_detail[name]['val']= this.state[name]['val']
      model_detail[name]['disabledButton']=true
      this.setState({model_details:model_detail})
    }  

    this.setState({disabled_button: this.errorSubmit()}) 
  }


  checkValidity = (name,value) => {
    if (value<=this.state.model_details[name]['hival'] && value >=this.state.model_details[name]['lowval']){
      if (this.state.model_details[name]['atype'] === 'INT' && !!(value%1)=== false){
        return 1
      }
      else if(this.state.model_details[name]['atype'] === 'DBL'){
        return 1
      }
      else {
        return -1
      }
    }
    else return 0
  }


  handleSubmit = event => {
    event.preventDefault();

    axios.put(this.api_server + this.state.id,this.state.model_details)
    .then(res => {
      console.log(res);
      console.log(res.data);
    },

    console.log(this.state.model_details))
    this.props.history.push({pathname:`/models/menu/${this.state.id}`,state: {
                menu_id: this.state.id,
                name: this.props.location.state.name
               }});
  }

  goback=()=>{
     this.props.history.goBack();
  }


  render() {
    const { disabled_button } = this.state;

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
        <h2 style={{ "textAlign": "center" }}>Please set the parameters for your model</h2>
        <h3 style={{ "textAlign": "left" }}> {this.props.location.state.name} </h3>
        <br /><br />
        <form>
          {Object.keys(this.state.model_details).map((item,i)=> {
          return(
            <label 
              key={i}>{this.state.model_details[item]['question']} {" "}
              <input type={this.state.model_details[item]['atype']} defaultValue={this.state.model_details[item]['val']} onChange={this.handleChange} name={item} />
              <span style={{color:"red",fontSize: 12}}>{this.state.model_details[item]['errorMessage']}</span>
              <br/><br/>
            </label>
          )})
          }
        </form>
        <br /><br />
        <button onClick={this.goback}>Go Back</button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <button disabled={disabled_button} onClick={!disabled_button ? this.handleSubmit : null}>Submit</button>
        
      </div>
    );
  }
}

export default ModelDetail;