import React, { Component } from 'react';
import { Loader, Dimmer } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import ListGroup from 'react-bootstrap/ListGroup';
import axios from 'axios';
import PopulationGraph from './PopulationGraph';
import ScatterPlot from './ScatterPlot';
import Debugger from './Debugger';
import PreFormTextBox from './PreFormTextBox';

const POP = 2;
const SCATTER = 3;
const DATA = 4;
const SOURCE = 5;
const API_SERVER = 'https://indrasnet.pythonanywhere.com/models/menu/';

class ActionMenu extends Component {
  constructor(props) {
    super(props);
    this.state = {
      msg: '',
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
    console.log(API_SERVER);
    this.setState({
      menu: m.data,
      name: localStorage.getItem('name'),
      modelId: localStorage.getItem('menu_id'),
      source: localStorage.getItem('source'),
      env_file: JSON.parse(localStorage.getItem('env_file')),
      msg: JSON.parse(localStorage.getItem('env_file')).user.user_msgs,
    });
    console.log(this.state);
  }

    viewSource = () => {
      window.open(localStorage.getItem('source'));
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
          this.viewSource();
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
      } catch (e) {
        console.log(e.message);
      }
    };

    renderHeader = () => {
      const { name } = this.state;
      return (
        <h1 style={{ textAlign: 'center', fontWeight: '200' }}>
          {name}
        </h1>
      );
    }

    MenuItem = (i, action, text) => (
      <ListGroup className="w-50 text-primary p-3 list-group-item list-group-item-action"
        key={i}
        onClick={() => this.handleClick(action)}
      >
        { text }
      </ListGroup>
    );

    renderModelStatus = () => {
      const { msg } = this.state;
      return (
        <div>
          <div
            className="card w-50 overflow-auto"
            style={{ float: 'right', width: '18rem', height: '18rem' }}
          >
            { PreFormTextBox('Model Status', msg) }
          </div>
        </div>
      );
    }

    renderDimmer = () => (
      <Dimmer active inverted>
        <Loader size="massive">Loading...</Loader>
      </Dimmer>
    );

    renderMenuItem = () => {
      const {
        loadingPopulation,
        env_file,
        modelId,
        loadingDebugger,
        loadingScatter,
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
            style={{ width: 30, height: 30 }}
            type="INT"
            className="from-control m-2"
            placeholder="10"
            onChange={this.handleRunPeriod}
          />
          {' '}
          periods.
          <span style={{ color: 'red', fontSize: 12 }}>
            {errorMessage}
          </span>
        </div>
      );
    }

  renderMapItem = () => {
    const { menu } = this.state;
    return (
      <div className="row">
        <div className="col">
          {
            Object.keys(menu).map((item, i) => (
              <div key={i}>
                {
                  menu[item].id > 1
                    ? this.MenuItem(
                      i,
                      menu[item].id,
                      menu[item].question,
                    )
                    : null
                }
              </div>
            ))
          }
        </div>
      </div>
    );
  }

  render() {
    const { loadingData } = this.state;
    if (loadingData) {
      return (
        <div className="container-fluid" style={{ height: 600 }}>
          <div className="row text-center" style={{ height: '100%' }}>
            <div className="col-12" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
              <div className="spinner-border" role="status">
                <span className="sr-only">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div>
        <br />
        <button type="button" className="btn btn-light m-2" onClick={this.goback}>Back</button>
        {this.renderHeader()}
        <br />
        <br />
        {this.renderModelStatus()}
        <ul className="list-group">
          <div className="row">
            <div>
              {this.renderRunButton()}
              <br />
              <br />
              <h3>Model Analysis:</h3>
              <br />
            </div>
          </div>
          {this.renderMapItem()}
        </ul>
        <br />
        <br />
        <br />
        <br />
        {this.renderMenuItem()}
      </div>
    );
  }
}

export default ActionMenu;
