import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

class Menu extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/menu/';
  state = {
  msg: '',
  menu_list:{},
  loadingData: false,
  model_id: 0,
  action_id: 0,
}

async componentDidMount() {
  this.setState({ loadingData: true });
  document.title = "Indra | Menu";
  const menu = await axios.get(this.api_server);
  this.setState({menu_list:menu.data})
  const {id} = this.props.match.params;
  this.setState({name:this.props.location.state.name})
  this.setState({model_id:id});
  console.log(this.state.menu_list)
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
        <h1 style={{ "textAlign": "center" }}>{this.state.name}
        </h1>

        <br /><br />

        { Object.keys(this.state.menu_list).map((item,i)=>
        <li key={i} >
          <Link to={{pathname:'/models/menu/', state: { menu_id: this.state.menu_list[item]['id'] }}}>
            {this.state.menu_list[item]['question']}
          </Link>
        </li>)}

        <br /><br />

      </div>
    );
  }
}

export default Menu;
