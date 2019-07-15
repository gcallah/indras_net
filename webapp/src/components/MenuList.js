import React, { Component } from "react";
import { Loader, Dimmer, Menu, Card} from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';
import PopulationGraph from "./PopulationGraph.js"
import ScatterPlot from "./ScatterPlot.js"
import Debugger from "./Debugger.js"

class MenuList extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/menu/';
  state = {
  msg: '',
  menu_list:{},
  loadingData: false,
  env_file: {},
  model_id: 0,
  action_id: 0,
  show_component: false,
  period_num: 10,
  errorMessage: "",
  disabled_button: false,
  loading_population:false,
  loading_scatter: false,
  loading_debugger: false
}

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Menu";
    const menu = await axios.get(this.api_server);
    this.setState({menu_list:menu.data})
    const id = localStorage.getItem("menu_id");
    const name = localStorage.getItem("name");
    this.setState({name:name})
    this.setState({model_id:id});
    this.setState({ loadingData: false });
    this.setState({env_file: this.props.location.state.env_file})
  }

  goback=()=>{
    this.props.history.replace({
      pathname: "/models/props/",
      state:{ menu_id: localStorage.getItem("menu_id"), name:localStorage.getItem("name")}
    });
  }

  onClick=()=> {
    this.setState({
      show_component: true,
    });
  }


  handleRunPeriod= e =>{
    this.setState({
      period_num: e.target.value
    })

    let valid = this.checkValidity(e.target.value)
    if (valid === 0){
      this.setState({errorMessage: '**Please input an integer'})
      this.setState({disabled_button: true})
    }
    else {
      this.setState({errorMessage: ''})
      this.setState({disabled_button: false})
    }
  }


  checkValidity = data => {
    let remainder = data%1
    if (remainder === 0){
      return 1
    }
    else return 0
  }

  handleClick= e =>{
    this.setState({loadingData: false})
    this.setState({loading_population: false})
    this.setState({loading_scatter:false})
    if (e === 2){
      this.setState({loading_scatter: false})
      this.setState({loading_debugger: false})
      this.setState({loading_population:true})
      this.setState({action_id: 2})
    }
    else if (e === 3){
      this.setState({loading_debugger: false})
      this.setState({loading_population: false})
      this.setState({loading_scatter:true})
      this.setState({action_id: 3})
    }
    else if (e === 4){
      this.setState({loading_population: false})
      this.setState({loading_scatter: false})
      this.setState({loading_debugger:true})
      this.setState({action_id: 4})
    }
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
        <h1 style={{ "textAlign": "center" }}>{this.state.name}
        </h1>

        <br /><br /> 
        <Card style={{ width: '30rem', height: '15rem', padding: '1rem', alignItems: 'center', float:'right', margin: 'auto', overflowY: 'scroll',}}>
          <Card.Content>
            <Card.Header>Update Status</Card.Header>
            {this.state.msg}
          </Card.Content>
        </Card>


        <Menu vertical style={{
          width: '30rem', 
          height: '15rem',
          overflowY: 'scroll',
        }}>

        { Object.keys(this.state.menu_list).map((item,i)=>
        <Menu.Item key={i}>
          {this.state.menu_list[item]['id']===0?<Link to={{pathname:'/', state: { action_id: this.state.menu_list[item]['id'] }}}>
            {this.state.menu_list[item]['question']}
          </Link>:null}

          {this.state.menu_list[item]['id']===1? <div>
          <button disabled={this.state.disabled_button} onClick={!this.state.disabled_button ? this.onClick : null}> Run </button>
          {" "}for <input style={{width: 30}} type='INT' defaultValue='10' onChange={this.handleRunPeriod} /> periods.
            <span style={{color:"red",fontSize: 12}}>{this.state.errorMessage}</span>
          </div>:null}

          {this.state.menu_list[item]['id']===2?<Link onClick={() => this.handleClick(2)}>
            {this.state.menu_list[item]['question']}
          </Link>:null}

          {this.state.menu_list[item]['id']===3?<Link onClick={() => this.handleClick(3)}>
            {this.state.menu_list[item]['question']}
          </Link>:null}

          {this.state.menu_list[item]['id']===4?<Link onClick={() => this.handleClick(4)}>
            {this.state.menu_list[item]['question']}
          </Link>:null}
        </Menu.Item>)}
        </Menu>
        <br /><br />
        <button onClick={this.goback}>Go Back</button>
        <br/><br/>
        <PopulationGraph loadingData={this.state.loading_population} env_file={this.state.env_file}/>
        <ScatterPlot loadingData={this.state.loading_scatter} env_file={this.state.env_file}/>
        <Debugger loadingData={this.state.loading_debugger} env_file={this.state.env_file}/>


      </div>
    );
  }
}

export default MenuList;
