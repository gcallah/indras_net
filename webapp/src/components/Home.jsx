import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Carousel from './Carousel';
import sandpileImg from './images/Sandpile.jpg';
import sandpile1Img from './images/sandpile_2.png';
import mandelobrotImg from './images/mendelobrot_sq.jpg';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      allItems: [],
      loadingData: false,
      dataForCarousel: [
        { image: sandpileImg, title: 'by Seth Terashima' },
        { image: sandpile1Img, title: 'by Colt Browninga' },
        { image: mandelobrotImg, title: 'by Adam majewski' },
      ],
    };
    this.api_server = 'https://indrasnet.pythonanywhere.com/';
  }

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      document.title = 'Indra | Home';
      const res = await axios.get(`${this.api_server }models`);
      this.setState({ allItems: res.data });
      this.setState({ loadingData: false });
      console.log('data-->', this.state.allItems);
    } catch (e) {
      console.log(e.message);
    }
  }

  openDescription = () => {
    const link = 'https://gcallah.github.io/indras_net/index.html';
    window.open(link);
  };

  renderShowDescription = () => {
    console.log('renderShowDescription called');
    return (
      <h1 style={{ fontSize: 16, fontWeight: '400' }}>
        <a href="#" className="text-primary m-2" onClick={this.openDescription}>
          View Project Description
          {' '}
        </a>
        {' '}
      </h1>
    );
  };

  handleClick(id, name, source) {
    console.log(localStorage);
    localStorage.setItem('menu_id', id);
    localStorage.setItem('name', name);
    localStorage.setItem('source', source);
  }

  renderHeader = () => <h1 className="text-center">Indra Agent-Based Modeling System</h1>;

  renderChooseModelProp = () => (
    <h1 style={{ fontSize: 16, fontWeight: '400' }}>
      Please choose a model:
      {' '}
    </h1>
  );

  render() {
    const { loadingData, dataForCarousel, allItems } = this.state;
    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading...</Loader>
        </Dimmer>
      );
    }
    return (
      <div className="container">
        <div style={{ marginBottom: 100 }}>{this.renderHeader()}</div>
        <div className="row">
          <div className="col-6">
            {this.renderChooseModelProp()}
            <ul className="list-group">
              <div className="row">
                <div className="col">
                  {Object.keys(allItems).map((item, i) => (
                    <li
                      className="w-75 p-3 list-group-item list-group-item-action"
                      key={i}
                    >
                      {console.log(allItems)}
                      <Link
                        to={{
                          pathname: `/models/props/${
                            allItems[item]['model ID']
                          }`,
                        }}
                        className="text-primary"
                        data-toggle="tooltip"
                        data-placement="top"
                        title={allItems[item].doc}
                        onClick={() => this.handleClick(
                          allItems[item]['model ID'],
                          allItems[item].name,
                          allItems[item].source,
                        )}
                      >
                        {allItems[item].name}
                      </Link>
                    </li>
                  ))}
                </div>
              </div>
            </ul>
            {this.renderShowDescription()}
          </div>
          <div className="col-6">
            <Carousel
              speed={5000}
              autoplay
              className="col-12"
              data={dataForCarousel}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
