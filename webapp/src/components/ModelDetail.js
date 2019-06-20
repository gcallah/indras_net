import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';
import { Link } from 'react-router-dom';

class ModelDetail extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/props/';
  state = {
    msg: '',
    model_detail: {},
    grid_height: {},
    grid_width: {},
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Property";
    const {menu_id} = this.props.location.state
    const res = await axios.get(this.api_server + menu_id.id)
    this.setState({ model_detail: res.data });
    this.setState({grid_height: res.data['grid_height']});
    this.setState({grid_width: res.data['grid_width']})
    this.setState({ loadingData: false });
    console.log(this.state.grid_height['val']);
  }
   handleChange = (event) => {
   //this.setState({ [target['val']]: target.value });
   this.setState({grid_height: event.target.value});
   console.log(this.state.grid_height['val']);
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
		<label>Grid Height :</label>
			<input type="int" defaultValue={this.state.grid_height['val']} onChange={this.updateState}/>
	        <br /><br/>
        </form>
        <br /><br />
      </div>
    );
  }
}

export default ModelDetail;
