/* eslint-disable react/no-array-index-key */
/* eslint-disable react/button-has-type */
/* eslint-disable react/prop-types */
/* eslint-disable camelcase */
/* eslint-disable react/no-access-state-in-setstate */
/* eslint-disable react/destructuring-assignment */
import React, { Component } from 'react';
import axios from 'axios';
import ModelInputField from './ModelInputField';
import PageLoader from './PageLoader';
import './styles.css';

const apiServer = 'https://indrasnet.pythonanywhere.com/models/props/';

class ModelDetail extends Component {
  constructor(props) {
    super(props);

    this.state = {
      modelDetails: {},
      loadingData: false,
      disabledButton: false,
      envFile: {},
    };
  }

  async componentDidMount() {
    const { modelDetails } = this.state;
    try {
      document.title = 'Indra | Property';
      this.setState({ loadingData: true });
      console.log(`${apiServer}${localStorage.getItem('menu_id')}`);
      const properties = await axios.get(`${apiServer}${localStorage.getItem('menu_id')}`);
      this.setState({ modelDetails: properties.data });
      console.log('modelDetail json', modelDetails);
      this.states(properties.data);
      this.errors(properties.data);
      this.setState({ loadingData: false });
    } catch (e) {
      console.log(e.message);
    }
  }


    states = (data) => {
      const { modelDetails } = this.state;
      // loop over objects in data and create object in this.state
      console.log(this.state);
      Object.keys(modelDetails).forEach((item) => this.setState({ [item]: data[item] }));
    }


    errors = () => {
      const { modelDetails } = this.state;
      Object.keys(modelDetails).forEach((item) => this.setState((prevState) => ({
        modelDetails: {
          ...prevState.modelDetails,
          [item]: {
            ...prevState.modelDetails[item],
            errorMessage: '',
            disabledButton: false,
          },
        },
      })));
    }


    errorSubmit = () => {
      const { modelDetails } = this.state;
      let ans = false;
      Object.keys(modelDetails).forEach((item) => {
        ans = ans || modelDetails[item].disabledButton;
      });
      return ans;
    }

    propChanged = (e) => {
      const { modelDetails } = this.state;
      const modelDetail = modelDetails;
      const { name, value } = e.target;
      const valid = this.checkValidity(name, value);
      modelDetail[name].disabledButton = true;

      if (valid === 1) {
        modelDetail[name].val = value;
        modelDetail[name].errorMessage = '';
        modelDetail[name].disabledButton = false;
        this.setState({ modelDetails: modelDetail });
      } else if (valid === -1) {
        modelDetail[name].errorMessage = '**Wrong Input Type';
        modelDetail[name].val = this.state[name].val;
        this.setState({ modelDetails: modelDetail });
        console.log(modelDetails[name]);
      } else {
        modelDetail[name].errorMessage = `**Please input a number between ${this.state[name].lowval} and ${this.state[name].hival}.`;
        modelDetail[name].val = this.state[name].val;
        this.setState({ modelDetails: modelDetail });
      }

      this.setState({ disabledButton: this.errorSubmit() });
    }


    checkValidity = (name, value) => {
      if (value <= this.state.modelDetails[name].hival
                && value >= this.state.modelDetails[name].lowval) {
        if (this.state.modelDetails[name].atype === 'INT'
                && !!(value % 1) === false) {
          return 1;
        }
        if (this.state.modelDetails[name].atype === 'DBL') {
          return 1;
        }

        return -1;
      }
      return 0;
    }


    handleSubmit = async (event) => {
      event.preventDefault();
      console.log(this.state.modelDetails);
      try {
        const res = await axios.put(apiServer + localStorage.getItem('menu_id'), this.state.modelDetails);
        const item_id = localStorage.getItem('menu_id');
        this.setState({ envFile: res.data });
        localStorage.setItem('envFile', JSON.stringify(this.state.envFile));
        this.props.history.push({
          pathname: `/models/menu/${item_id.toString(10)}`,
          state: {
            envFile: this.state.envFile,
          },
        });
      } catch (e) {
        console.log(e.message);
        this.props.history.push('/errorCatching');
      }
    }

    renderHeader = () => (
      <h1 className="header" style={{ textAlign: 'center', fontWeight: '200' }}>
        {' '}
Please set the parameters for the
        {' '}
        {localStorage.getItem('name')}
        {' '}
model
      </h1>
    )

    renderSubmitButton = () => {
      const { disabledButton } = this.state;
      return (
        <button
          disabled={disabledButton}
          onClick={!disabledButton ? this.handleSubmit : null}
          className="btn btn-primary m-2"
        >
Submit

        </button>
      );
    }

    goback=() => {
      this.props.history.goBack();
    }

    render() {
      if (this.state.loadingData) {
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
              {Object.keys(this.state.modelDetails).map((item, i) => {
                if ('question' in this.state.modelDetails[item]) {
                  return (
                    <ModelInputField
                      label={this.state.modelDetails[item].question}
                      type={this.state.modelDetails[item].atype}
                      placeholder={this.state.modelDetails[item].val}
                      error={this.state.modelDetails[item].errorMessage}
                      propChange={this.propChanged}
                      name={item}
                      key={i}
                    />
                  );
                }
                return null;
              })}
            </div>
          </form>
          <br />
          <br />
          {this.renderSubmitButton()}
        </div>
      );
    }
}

export default ModelDetail;
