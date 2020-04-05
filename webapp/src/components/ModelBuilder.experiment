import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import ModelInputField from './ModelInputField';
import PageLoader from './PageLoader';
import './styles.css';

const apiServer = 'https://indrasnet.pythonanywhere.com/models/props/';

class ModelBuilder extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loadingData: false,
      disabledButton: false,
    };
  }

  async componentDidMount() {
    const { history } = this.props;
    try {
      document.title = 'Indra | Property';
      this.setState({ loadingData: true });
      const properties = await axios.get(`${apiServer}${localStorage.getItem('menu_id')}`);
      this.states(properties.data);
      this.errors(properties.data);
      this.setState({ loadingData: false });
    } catch (e) {
      history.push('/errorCatching');
    }
  }

    renderHeader = () => (
        <h1 className="header" style={{ textAlign: 'center', fontWeight: '200' }}>
        Please set the parameters for the model builder
        </h1>
    )

    renderSubmitButton = () => {
      const { disabledButton } = this.state;
      return (
        <button
          type="button"
          disabled={disabledButton}
          onClick={!disabledButton ? this.handleSubmit : null}
          className="btn btn-primary m-2"
        >
          Submit
        </button>
      );
    }

    goback=() => {
      const { history } = this.props;
      history.goBack();
    }

    render() {
      const { loadingData } = this.state;
      if (loadingData) {
        return (
          <PageLoader />
        );
      }
      return (
        <div>
          <h1 className="margin-top-60"> </h1>
          {this.renderHeader()}
          <br />
          <br />
          <form>
            <div className="container">
              <ModelInputField
                label="What is the grid height?"
                type="INT"
                placeholder="20"
                propChange={this.propChanged}
                name="height"
              />
            </div>
          </form>
          <br />
          <br />
          {this.renderSubmitButton()}
        </div>
      );
    }
}

ModelBuilder.propTypes = {
  history: PropTypes.shape(),
};

ModelBuilder.defaultProps = {
  history: {},
};

export default ModelBuilder;
