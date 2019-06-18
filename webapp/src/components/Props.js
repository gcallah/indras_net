import React, { Component } from "react";
import { Loader, Dimmer, Menu} from "semantic-ui-react";
class Props extends Component {
  state = {
    msg: '',
    loadingData: false,
  }
  //id is in props

  //request API server with id for specific model - props 
  //return what API return

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Indra | Work in Progress";
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
    console.log('ONCLICK')
    console.log(this.props.item['model ID'])
    return (
      <div>
        <br />
        <h1 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!
        </h1>
        <br /><br />
        <Menu.Item key={this.props.id} onClick={() => this.props.handleChange(this.props.item['model ID'])}>
        </Menu.Item>     
      </div>
    );
  }
}

export default Props;
