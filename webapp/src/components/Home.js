import React, {Component} from 'react';
import {Loader, Dimmer} from 'semantic-ui-react';
import ListGroup from 'react-bootstrap/ListGroup';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import axios from 'axios';
<<<<<<< HEAD
import {Link} from 'react-router-dom';
=======
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
import Carousel from './Carousel';
import sandpileImg from './images/Sandpile.jpg';
import sandpile1Img from './images/sandpile_2.png';
import mandelobrotImg from './images/mendelobrot_sq.jpg';
import './styles.css';

class Home extends Component {
  constructor (props) {
    super (props);
    this.state = {
      allItems: [],
      loadingData: false,
      apiFailed: false,
      dataForCarousel: [
        {image: sandpileImg, title: 'by Seth Terashima'},
        {image: sandpile1Img, title: 'by Colt Browninga'},
        {image: mandelobrotImg, title: 'by Adam majewski'},
      ],
    };
    this.api_server = 'https://indrasnet.pythonanywhere.com/';
  }

<<<<<<< HEAD
  async componentDidMount () {
=======
  async componentDidMount() {
    const { history } = this.props;
>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
    try {
      this.setState ({loadingData: true});
      document.title = 'Indra | Home';
      const res = await axios.get (`${this.api_server}models`);
      this.setState ({allItems: res.data, loadingData: false});
    } catch (e) {
<<<<<<< HEAD
      this.setState ({apiFailed: true});
    }
  }

  renderShowDescription = () => (
    <h1 className="small-header">
      <a
        href="https://gcallah.github.io/indras_net/index.html"
        className="text-primary m-2"
        target="_blank"
        rel="noopener noreferrer"
      >
        View Project Description
        {' '}
      </a>
      {' '}
    </h1>
  );

=======
      history.push('/errorCatching');
    }
  }

>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
  handleClick = (id, name, source) => {
    localStorage.setItem ('menu_id', id);
    localStorage.setItem ('name', name);
    localStorage.setItem ('source', source);
  };

<<<<<<< HEAD
  renderHeader = () => (
    <h1 className="text-center">Indra Agent-Based Modeling System</h1>
  );

=======
>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
  renderChooseModelProp = () => (
    <h1 className="small-header">
      Please choose a model:
      {' '}
    </h1>
  );

  render () {
    const {loadingData, dataForCarousel, allItems, apiFailed} = this.state;
    if (apiFailed) {
      return <h1>404 Error</h1>;
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
<<<<<<< HEAD
        <h1 className="margin-top-60"> </h1>
        <div className="margin-bottom-100">{this.renderHeader ()}</div>
=======
        <div className="margin-bottom-80">
          <h1 className="text-left">The Agent-Based Modeling System</h1>
        </div>
>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
        <div className="row">
          <div className="col-6">
            {this.renderChooseModelProp ()}
            <ListGroup>
              {Object.keys (allItems).map (item => (
                <OverlayTrigger
                  key={`${allItems[item].name}-tooltip`}
                  placement="right"
                  overlay={
                    <Tooltip>
                      {allItems[item].doc}
                    </Tooltip>
                  }
                >
                  <Link
                    to={{
                      pathname: `/models/props/${allItems[item]['model ID']}`,
                    }}
<<<<<<< HEAD
                    className="text-primary w-75 p-3 list-group-item list-group-item-action borderless"
=======
                    className="text-primary w-75 p-3 list-group-item list-group-item-action link"
>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
                    key={allItems[item].name}
                    onClick={() =>
                      this.handleClick (
                        allItems[item]['model ID'],
                        allItems[item].name,
                        allItems[item].source
                      )}
                  >
                    {allItems[item].name}
                  </Link>
                </OverlayTrigger>
              ))}
            </ListGroup>
<<<<<<< HEAD
            {this.renderShowDescription ()}
=======
>>>>>>> 65895954962dcf16b51cbefcf854e6b554891476
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

Home.propTypes = {
  history: PropTypes.shape(),
};

Home.defaultProps = {
  history: {},
};

export default Home;
