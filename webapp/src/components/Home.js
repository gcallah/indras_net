import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import ListGroup from 'react-bootstrap/ListGroup';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/ToolTip';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Carousel from './Carousel';
import sandpileImg from './images/Sandpile.jpg';
import sandpile1Img from './images/sandpile_2.png';
import mandelobrotImg from './images/mendelobrot_sq.jpg';
import './styles.css';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      allItems: [],
      loadingData: false,
      apiFailed: false,
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
      const res = await axios.get(`${this.api_server}models`);
      this.setState({ allItems: res.data, loadingData: false });
    } catch (e) {
      this.setState({ apiFailed: true });
    }
  }

  renderShowDescription = () => (
    <h1 className="small-header">
      <a href="https://gcallah.github.io/indras_net/index.html" className="text-primary m-2" target="_blank" rel="noopener noreferrer">
        View Project Description
        {' '}
      </a>
      {' '}
    </h1>
  );

  handleClick = (id, name, source) => {
    localStorage.setItem('menu_id', id);
    localStorage.setItem('name', name);
    localStorage.setItem('source', source);
  }

  renderHeader = () => <h1 className="text-center">Indra Agent-Based Modeling System</h1>;

  renderChooseModelProp = () => (
    <h1 className="small-header">
      Please choose a model:
      {' '}
    </h1>
  );

  render() {
    const {
      loadingData, dataForCarousel, allItems, apiFailed,
    } = this.state;
    if (apiFailed) {
      return (
        <h1>404 Error</h1>
      );
    }
    if (loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading...</Loader>
        </Dimmer>
      );
    }
    return (
      <div className="container">
        <h1 className= "margin-top-60"> </h1> 
        <div className="margin-bottom-100">{this.renderHeader()}</div>
        <div className="row">
          <div className="col-6">
            {this.renderChooseModelProp()}
            <ListGroup>
              {Object.keys(allItems).map((item) => (
                <OverlayTrigger
                  key={`${allItems[item].name}-tooltip`}
                  placement="right"
                  overlay={(
                    <Tooltip>
                      {allItems[item].doc}
                    </Tooltip>
                  )}
                >
                  <Link
                    to={{
                      pathname: `/models/props/${
                        allItems[item]['model ID']
                      }`,
                    }}
                    className="text-primary w-75 p-3 list-group-item list-group-item-action"
                    key={allItems[item].name}
                    onClick={() => this.handleClick(
                      allItems[item]['model ID'],
                      allItems[item].name,
                      allItems[item].source,
                    )}
                  >
                    {allItems[item].name}
                  </Link>
                </OverlayTrigger>
              ))}
            </ListGroup>
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
