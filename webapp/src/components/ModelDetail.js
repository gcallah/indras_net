import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import ModelInputField from './ModelInputField';
import PageLoader from './PageLoader';
import './styles.css';
import config from '../config';

const apiServer = `${config.API_URL}models/props/`;

class ModelDetail extends Component {
  constructor(props) {
    super(props);
    const initialModelDetailState = this.getInitialModelDetails();
    this.state = {
      modelDetails: {},
      loadingData: false,
      disabledButton: false,
      ...initialModelDetailState,
    };
  }

  async componentDidMount() {
    const { history } = this.props;
    const { menuId } = this.state;
    try {
      document.title = 'Indra | Property';
      this.setState({ loadingData: true });
      const properties = await axios.get(
        `${apiServer}${menuId}`,
      );
      this.setState({ modelDetails: properties.data });
      this.states(properties.data);
      this.errors(properties.data);
      this.setState({ loadingData: false });
    } catch (e) {
      history.push('/errorCatching');
    }
  }

  getInitialModelDetails() {
    const { location, history, match } = this.props;
    let initialState;
    try {
      const { state } = location;
      if (state === undefined) {
      // this is undefined when someone tried to open the model in a new tab from the home screen.
        const menuId = parseInt(match.params.id, 10);
        const modalDetails = JSON.parse(localStorage.getItem('indra_model_details')).filter((item) => item['model ID'] === menuId)[0];
        initialState = {
          menuId,
          name: modalDetails.name,
          source: modalDetails.source,
          graph: modalDetails.graph,
        };
      } else {
        initialState = state;
      }
    } catch (err) {
      history.push('/errorCatching');
    }
    return initialState;
  }

  states = (data) => {
    const { modelDetails } = this.state;
    // loop over objects in data and create object in this.state
    Object.keys(modelDetails).forEach((detailName) => {
      this.setState((prevState) => ({
        modelDetails: {
          ...prevState.modelDetails,
          [detailName]: {
            ...prevState.modelDetails[detailName],
            defaultVal: data[detailName].val,
          },
        },
      }));
      // Object.keys(modelDetails).forEach((item) => this.setState({ [item]: data[item] }));
    });
  };

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
  };

  errorSubmit = () => {
    const { modelDetails } = this.state;
    let ans = false;
    Object.keys(modelDetails).forEach((item) => {
      ans = ans || modelDetails[item].disabledButton;
    });
    return ans;
  };

  propChanged = (e) => {
    const { modelDetails } = this.state;
    const { name, value } = e.target;
    const valid = this.checkValidity(name, value);
    modelDetails[name].disabledButton = true;

    if (valid === 1) {
      modelDetails[name].val = parseInt(value, 10);
      modelDetails[name].errorMessage = '';
      modelDetails[name].disabledButton = false;
      this.setState({ modelDetails });
    } else if (valid === -1) {
      modelDetails[name].errorMessage = '**Wrong Input Type';
      modelDetails[name].val = modelDetails[name].defaultVal;
      this.setState({ modelDetails });
    } else {
      modelDetails[
        name
      ].errorMessage = `**Please input a number between ${modelDetails[name].lowval} and ${modelDetails[name].hival}.`;
      modelDetails[name].val = modelDetails[name].defaultVal;
      this.setState({ modelDetails });
    }

    this.setState({ disabledButton: this.errorSubmit() });
  };

  checkValidity = (name, value) => {
    const { modelDetails } = this.state;
    if (
      value <= modelDetails[name].hival
      && value >= modelDetails[name].lowval
    ) {
      if (modelDetails[name].atype === 'INT' && !!(value % 1) === false) {
        return 1;
      }
      if (modelDetails[name].atype === 'DBL') {
        return 1;
      }

      return -1;
    }
    return 0;
  };

  handleSubmit = async (event) => {
    event.preventDefault();
    const {
      modelDetails, menuId, name, source, graph,
    } = this.state;
    const { history } = this.props;
    try {
      // res gives us back the model returned from put props
      const res = await axios.put(
        apiServer + menuId,
        modelDetails,
      );
      const itemId = menuId;
      const envFile = res.data;
      const execKey = res.data.exec_key;
      history.push({
        pathname: `/models/menu/${itemId.toString(10)}`,
        state: {
          envFile,
          name,
          source,
          graph,
          execKey,
        },
      });
    } catch (e) {
      history.push('/errorCatching');
    }
  };

  renderHeader = () => {
    const { name } = this.state;
    return (
      <h1 className="header" style={{ textAlign: 'center', fontWeight: '200' }}>
        {`Please set the parameters for the ${name} model`}
      </h1>
    );
  };

  renderSubmitButton = () => {
    const { disabledButton } = this.state;
    // console.log(this.state);
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
  };

  goback = () => {
    const { history } = this.props;
    history.goBack();
  };

  render() {
    const { loadingData, modelDetails } = this.state;
    if (loadingData) {
      return <PageLoader />;
    }
    return (
      <div>
        <h1 className="margin-top-60"> </h1>
        {this.renderHeader()}
        <br />
        <br />
        <form>
          <div className="container">
            {Object.keys(modelDetails).map((item) => {
              if ('question' in modelDetails[item]) {
                return (
                  <ModelInputField
                    label={modelDetails[item].question}
                    type={modelDetails[item].atype}
                    placeholder={modelDetails[item].val}
                    error={modelDetails[item].errorMessage}
                    propChange={this.propChanged}
                    name={item}
                    key={item}
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

ModelDetail.propTypes = {
  history: PropTypes.shape(),
  location: PropTypes.shape({
    state: PropTypes.shape({
      menuId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
      name: PropTypes.string,
      source: PropTypes.string,
      graph: PropTypes.string,
    }),
  }),
  match: PropTypes.shape({
    params: PropTypes.shape({
      id: PropTypes.string,
    }),
  }),
};

ModelDetail.defaultProps = {
  history: {},
  location: {
    state: {},
  },
  match: {
    params: {
      id: '',
    },
  },
};

export default ModelDetail;
