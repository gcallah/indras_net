import React, { Component } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import axios from 'axios';
import autoBind from 'react-autobind';
import PropTypes from 'prop-types';
import PageLoader from './PageLoader';
import PopulationGraph from './PopulationGraph';
import PopulationBarGraph from './PopulationBarGraph';
import ScatterPlot from './ScatterPlot';
import Debugger from './Debugger';
import ModelStatusBox from './ModelStatusBox';
import SourceCodeViewer from './SourceCodeViewer';
import RunModelButton from './RunModelButton';
import './styles.css';
import config from '../config';
import LogsViewer from './LogsViewer';


const POP = 2;
const SCATTER = 3;
const BAR = 4;
// const DATA = 4;
const DEBUG = 5;
const SOURCE = 6;
const LOG = 7;
const API_SERVER = `${config.API_URL}models/menu/`;
const CLEAR_REGISTRY_API = `${config.API_URL}registry/clear/`;

class ActionMenu extends Component {
  constructor(props) {
    super(props);
    const { location } = this.props;
    const { state } = location;
    const { envFile } = state;
    this.state = {
      menu: {},
      loadingData: true,
      envFile: {},
      source: '',
      periodNum: 10,
      errorMessage: '',
      disabledButton: false,
      loadingSourceCode: false,
      loadingDebugger: false,
      loadingPopulation: false,
      loadingScatter: false,
      loadingBar: false,
      loadingLogs: false,
      activeDisplay: null,
      continuousRun: true,
      continuousRunDisabled: false,
      initLoading: true,
      EXECUTION_KEY: envFile.exec_key,
    };
    autoBind(this);
  }

  async componentDidMount() {
    const { EXECUTION_KEY } = this.state;
    const { location } = this.props;
    const { state } = location;
    const {
      envFile, name, source, graph,
    } = state;
    try {
      document.title = 'Indra | Menu';
      // you need to pass the execution key that you get from put_props
      // which is in ModelDetail, the current execution key is undefined
      const m = await axios.get(`${API_SERVER}${EXECUTION_KEY}`);
      // debugger;
      this.setState({
        menu: m.data,
        name,
        source,
        envFile,
        graph,
        msg: envFile.user.user_msgs,
        loadingData: false,
      });
    } catch (error) {
      return false;
    }
    const defaultGraph = graph;
    if (defaultGraph === 'scatter') {
      this.setState({
        loadingScatter: true,
        activeDisplay: SCATTER,
      });
    } else {
      this.setState({
        loadingPopulation: true,
        activeDisplay: POP,
      });
    }
    try {
      const code = await this.viewSource();
      this.setState({
        sourceCode: code,
      });
    } catch (error) {
      return false;
    }
    return true;
  }

  async componentWillUnmount() {
    // clear the registry in the backend.
    const { EXECUTION_KEY } = this.state;
    await axios.get(
      `${CLEAR_REGISTRY_API}${EXECUTION_KEY}`,
    );
    // not doing anything with the response.
    // allow the frontend to continue functioning.
    // there should be a error reporting mechanism here to notify
    // admins that a particular key was not cleared.
  }


  viewSource = async () => {
    try {
      const { source } = this.state;
      const splitSource = source.split('/');
      const filename = splitSource[splitSource.length - 1];
      const res = await axios.get(
        `https://raw.githubusercontent.com/gcallah/indras_net/master/models/${filename}`,
      );
      return res.data;
    } catch (error) {
      return 'Something has gone wrong.';
    }
  };

  handleRunPeriod = (e) => {
    this.setState({
      periodNum: e.target.value,
    });

    const valid = this.checkValidity(e.target.value);
    if (valid === 0) {
      this.setState({
        errorMessage: '**Please input an integer',
        disabledButton: true,
      });
    } else {
      this.setState({
        errorMessage: '',
        disabledButton: false,
      });
    }
  };

  checkValidity = (data) => {
    if (data % 1 === 0) {
      return 1;
    }
    return 0;
  };

  handleClick = (e) => {
    this.setState({
      loadingData: false,
      loadingSourceCode: false,
      loadingDebugger: false,
      loadingScatter: false,
      loadingPopulation: false,
      loadingLogs: false,
      loadingBar: false,
    });
    this.setState({
      activeDisplay: e,
    });
    switch (e) {
      case POP:
        this.setState({ loadingPopulation: true });
        break;
      case SCATTER:
        this.setState({ loadingScatter: true });
        break;
      case DEBUG:
        this.setState({ loadingDebugger: true });
        break;
      case SOURCE:
        this.setState({ loadingSourceCode: true });
        break;
      case LOG:
        this.setState({ loadingLogs: true });
        break;
      case BAR:
        this.setState({ loadingBar: true });
        break;
      default:
        break;
    }
  };

  sendNumPeriods = async () => {
    const { periodNum, envFile, EXECUTION_KEY } = this.state;
    const envFileWithExecutionKey = { ...envFile, execution_key: EXECUTION_KEY };
    this.setState({ loadingData: true });
    try {
      const res = await axios.put(
        `${config.API_URL}models/run/${String(periodNum)}`,
        envFileWithExecutionKey,
        periodNum,
      );

      this.setState({
        envFile: res.data,
        loadingData: false,
        msg: res.data.user.user_msgs,
      });
      // return true;
    } catch (e) {
      // return false;
    }
  };

  timeout = (m) => new Promise((r) => setTimeout(r, m))

  continuousRun = async () => {
    this.setState(
      {
        continuousRun: true,
        continuousRunDisabled: true,
        periodNum: 1,
        initLoading: false,
      },
    );
    await this.timeout(200);
    /* eslint-disable */
    while (this.state.continuousRun) {
      // this.setState({periodNum: 1});
      this.sendNumPeriods();
      /* eslint-disable */
      while (this.state.loadingData){
        await this.timeout(200);
      /* eslint-disable */
        console.log('still waiting for data...')
      }
      /* eslint-disable */
      console.log('data arrived!!')
    }
  }

  stopRun = () => {
    this.setState(
      {
        continuousRun: false,
        continuousRunDisabled: false,
      },
    );
  }

  renderHeader = () => {
    const { name } = this.state;
    return <h1 className="header">{name}</h1>;
  };

  MenuItem = (i, action, text, key) => {
    /**
     * All models will have all the menu items appear on the page.
     * However, we keep one of the graphs (Population graph or Scatter plot)
     * disabled based on "graph" field from models.json
     */
    const { graph } = this.state;
    const defaultGraph = graph;
    const { activeDisplay } = this.state;
    return (
      <ListGroup.Item
        className="w-50 p-3 list-group-item list-group-item-action"
        as="li"
        active={activeDisplay === action}
        disabled={
          (action === SCATTER && defaultGraph === 'line')
          || (action === POP && defaultGraph === 'scatter')
        }
        key={key}
        onClick={() => this.handleClick(action)}
      >
        {text}
      </ListGroup.Item>
    );
  };

  renderMenuItem = () => {
    const {
      envFile,
      loadingDebugger,
      loadingSourceCode,
      sourceCode,
      loadingPopulation,
      loadingScatter,
      loadingLogs,
      loadingBar
    } = this.state;
    return (
      <div className="mt-5">
        <Debugger loadingData={loadingDebugger} envFile={envFile} />
        <SourceCodeViewer loadingData={loadingSourceCode} code={sourceCode} />
        <PopulationGraph loadingData={loadingPopulation} envFile={envFile} />
        <PopulationBarGraph loadingData={loadingBar} envFile={envFile} />
        <ScatterPlot loadingData={loadingScatter} envFile={envFile} />
        <LogsViewer loadingData={loadingLogs} envFile={envFile} />
      </div>
    );
  };

  renderMapItem = () => {
    const { menu } = this.state;
    return (
      <div className="row margin-bottom-80">
        <div className="col w-25">
          <ListGroup>
            {Object.keys(menu).map((item, i) => (menu[item].id > 1
              ? this.MenuItem(
                i,
                menu[item].id,
                menu[item].question,
                menu[item].func,
              )
              : null))}
          </ListGroup>
        </div>
      </div>
    );
  };

  render() {
    const {
      loadingData, msg, disabledButton, errorMessage, initLoading, continuousRunDisabled,
    } = this.state;
    if (loadingData && initLoading) {
      return <PageLoader />;
    }
    // if (loadingData && !initLoading){
    //   return;
    // }
    return (
      <div>
        {this.renderHeader()}
        <div>
          <ModelStatusBox
            title="Model Status"
            msg={msg}
            ref={this.modelStatusBoxElement}
          />
        </div>
        <ul className="list-group">
          <div className="row">
            <div>
              <RunModelButton
                disabledButton={disabledButton}
                errorMessage={errorMessage}
                sendNumPeriods={this.sendNumPeriods}
                handleRunPeriod={this.handleRunPeriod}
              />
              {/* eslint-disable */}
              <button
                onClick={this.continuousRun}
                disabled={continuousRunDisabled}
                className="btn btn-success m-2"
              >
                Continuous Run
              </button>
              {/* eslint-disable */}
              <button
                onClick={this.stopRun}
                className="btn btn-danger m-2"
              >
                Stop
              </button>
              <h3 className="margin-top-50 mb-4">Model Analysis:</h3>
            </div>
          </div>
          {this.renderMapItem()}
        </ul>
        {this.renderMenuItem()}
      </div>
    );
  }
}

ActionMenu.propTypes = {
  location: PropTypes.shape({
    state: PropTypes.shape({
      envFile: PropTypes.object,
      name: PropTypes.string,
      source: PropTypes.string,
      graph: PropTypes.string,
    }),
  }),
  /* eslint-disable */
  history: PropTypes.object,
};

ActionMenu.defaultProps = {
  location: {
    state: {
      envFile: {},
    },
  },
  history: {},
};

export default ActionMenu;
