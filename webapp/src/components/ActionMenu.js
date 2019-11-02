import React, { Component } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import axios from 'axios';
import PageLoader from './PageLoader';
import PopulationGraph from './PopulationGraph';
import ScatterPlot from './ScatterPlot';
import Debugger from './Debugger';
import PreFormTextBox from './PreFormTextBox';
import ModelStatusBox from './ModelStatusBox';
import autoBind from 'react-autobind';
import SourceCodeViewer from './SourceCodeViewer';
import './styles.css';


const POP = 2;
const SCATTER = 3;
const DATA = 4;
const SOURCE = 5;
const API_SERVER = 'https://indrasnet.pythonanywhere.com/models/menu/';

class ActionMenu extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.state = {
      msg: 'Please run model in order to retrieve data',
      menu: {},
      loadingData: false,
      env_file: {},
      modelId: 0,
      actionId: 0,
      showComponent: false,
      periodNum: 10,
      errorMessage: '',
      disabledButton: false,
      loadingPopulation: false,
      loadingScatter: false,
      loadingDebugger: false,
      
    };
  }

  async componentDidMount() {
    document.title = 'Indra | Menu';
    const m = await axios.get(API_SERVER);
    const code = await this.viewSource();
    console.log(API_SERVER);
    this.setState({
      menu: m.data,
      name: localStorage.getItem('name'),
      modelId: localStorage.getItem('menu_id'),
      source: localStorage.getItem('source'),
      env_file: JSON.parse(localStorage.getItem('env_file')),
      msg: JSON.parse(localStorage.getItem('env_file')).user.user_msgs,
      sourceCode: code,
    });
    console.log(this.state);
  }

  viewSource = async() => {
    try {
      const splitSource = localStorage.getItem('source').split('/')
      const filename = splitSource[splitSource.length - 1]
      const res = await axios.get(
        `https://raw.githubusercontent.com/gcallah/indras_net/master/models/${filename}`
      );
      console.log(res.data);
      return res.data;
    } catch(e) {
      console.log(e);
    }
  };
  onClick = () => {
    this.setState({
      showComponent: true,
    });
  };

  goback = () => {
    const { history } = this.props;
    history.goBack();
  }

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
    console.log(`e = ${String(e)}`);
    this.setState({
      loadingData: false,
      loadingPopulation: false,
      loadingScatter: false,
      loadingDebugger: false,
      actionId: e,
    });
    switch (e) {
      case POP:
        this.setState({ loadingPopulation: true });
        break;
      case SCATTER:
        this.setState({ loadingScatter: true });
        break;
      case DATA:
        this.setState({ loadingDebugger: true });
        break;
      case SOURCE:
        this.setState({ loadingSourceCode: true });
        break;
      default:
        break;
    }
  };

  sendNumPeriods = async () => {
    const { periodNum, env_file } = this.state;
    console.log(`${API_SERVER}run/${String(periodNum)}`);
    this.setState({ loadingData: true });
    try {
      const res = await axios.put(
        `${API_SERVER}run/${String(periodNum)}`,
        env_file,
        periodNum,
      );

      this.setState({
        env_file: res.data,
        loadingData: false,
        msg: res.data.user.user_msgs,
      });
      console.log(res.data);
      console.log("message is ", this.state.msg)
    } catch (e) {
      console.log(e.message);
    }
  };

  renderHeader = () => {
    const { name } = this.state;
    return (
      <h1 className="header">
        {name}
      </h1>
    );
  }

  MenuItem = (i, action, text, key) => (
    <ListGroup.Item
      className="w-50 text-primary p-3 list-group-item list-group-item-action"
      key={key}
      onClick={() => this.handleClick(action)}
    >
      { text }
    </ListGroup.Item>
  );

  renderModelStatus = () => {
    return (
      
      <div>
        <div className="card w-50 overflow-auto model-status">
      
          { PreFormTextBox('Model Status', this.state.msg) }
        </div>
      </div>
    );
  }

  renderMenuItem = () => {
    const {
      loadingPopulation,
      env_file,
      modelId,
      loadingDebugger,
      loadingScatter,
      loadingSourceCode,
      sourceCode
    } = this.state;
    return (
      <div>
        <PopulationGraph
          loadingData={loadingPopulation}
          env_file={env_file}
          id={modelId}
        />

        <ScatterPlot
          loadingData={loadingScatter}
          env_file={env_file}
          id={modelId}
        />

        <Debugger
          loadingData={loadingDebugger}
          env_file={env_file}
        />

        <SourceCodeViewer
          loadingData={loadingSourceCode}
          code={sourceCode}
        />
      </div>
    );
  }

  renderRunButton = () => {
    const { disabledButton, errorMessage } = this.state;
    return (
      <div>
        <button
          type="button"
          disabled={disabledButton}
          onClick={!disabledButton ? this.sendNumPeriods : null}
          className="btn btn-success m-2"
        >
          {'  '}
          Run
          {'  '}
        </button>
        {' '}
        <span>model for</span>
        {' '}
        <input
          type="INT"
          className="from-control m-2 number-input"
          placeholder="10"
          onChange={this.handleRunPeriod}
        />
        {' '}
        periods.
        <span className="error-message">
          {errorMessage}
        </span>
      </div>
    );
  }

  renderMapItem = () => {
    const { menu } = this.state;
    return (
      <div className="row margin-bottom-80">
        <div className="col">
          <ListGroup>
            {
              Object.keys(menu).map((item, i) => (
                menu[item].id > 1
                  ? this.MenuItem(
                    i,
                    menu[item].id,
                    menu[item].question,
                    menu[item].func,
                  )
                  : null
              ))
            }
          </ListGroup>
        </div>
      </div>
    );
  }

  render() {
    const { loadingDatam } = this.state;
    
    if (loadingDatam) {
      return (
        <PageLoader />
      );
    }
    return (
     
      <div>
        <br />
        {this.renderHeader()}
        <div>
        <ModelStatusBox title='Model Status' msg={this.state.msg} ref={this.modelStatusBoxElement}/>
        </div>
        <ul className="list-group">
          <div className="row">
            <div>
            
              {this.renderRunButton()}
              <h3 className="margin-top-60 mb-5">Model Analysis:</h3>
            </div>
          </div>
          {this.renderMapItem()}
        </ul>
        {this.renderMenuItem()}
      </div>
    );
  }
}

export default ActionMenu;
