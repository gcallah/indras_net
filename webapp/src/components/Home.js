import React, { Component } from "react";
import { Loader, Dimmer, Menu } from "semantic-ui-react";
import axios from 'axios';

class Home extends Component {
  state = {
    msg: '',
    allItems: [],
    loadingData: false,
  }

  async componentDidMount() {
    this.setState({ loadingData: true });
    document.title = "Title";
    const res = await axios.get('http://indrasnet.pythonanywhere.com/models')
    this.setState({ allItems: res.data });
    console.log(res.data);
    this.setState({ loadingData: false });
  }

  renderMenu = () => {
    let items = this.state.allItems.map((item, id) => {
      return (
        <Menu.Item
          key={id}
          name={item.name}
          href='/'
        >
        </Menu.Item>
      );
    });

    return <Menu vertical style={{
      maxHeight: '20em',
      maxwidth: '40em',
      overflowY: 'scroll',
    }}>{items}</Menu>;
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
        <h1 style={{ "textAlign": "center" }}>Welcome!</h1>
        <br /><br />

        We have several models:
        {this.state.allItems && this.renderMenu()}

        <br /><br />
      </div>
    );
  }
}

export default Home;
