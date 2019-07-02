import React, { Component } from "react";
import { Loader, Dimmer, Menu } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

class MenuList extends Component {
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
  console.log(this.state.model_id);
  this.setState({ loadingData: false });
}

 goback=()=>{
     this.props.history.replace({
         pathname: `/models/props/${this.state.model_id}`,
        state:{ menu_id: this.state.model_id, name:this.state.name}
       });
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
        <Menu vertical style={{
          maxHeight: '30em',
          maxwidth: '40em',
          overflowY: 'scroll',
        }}>
        { Object.keys(this.state.menu_list).map((item,i)=>
        <Menu.Item key={i} style={{fontSize:'1.3em'}}>
          {this.state.menu_list[item]['id']===0?<Link to={{pathname:'/', state: { menu_id: this.state.menu_list[item]['id'] }}}>
            {this.state.menu_list[item]['question']}
          </Link>:<Link to={{pathname:'/models/menu/', state: { menu_id: this.state.menu_list[item]['id'] }}}>
            {this.state.menu_list[item]['question']}
          </Link>}
        </Menu.Item>)}
        </Menu>
        <br /><br />
        <button onClick={this.goback}>Go Back</button>

      </div>
    );
  }
}

export default MenuList;
