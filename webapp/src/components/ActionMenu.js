import React, { Component } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import axios from 'axios';
import autoBind from 'react-autobind';
import PageLoader from './PageLoader';
// import PopulationGraph from './PopulationGraph';
// import ScatterPlot from './ScatterPlot';
import Debugger from './Debugger';
import ModelStatusBox from './ModelStatusBox';
import SourceCodeViewer from './SourceCodeViewer';
import RunModelButton from './RunModelButton';
import './styles.css';

const POP = 2;
const SCATTER = 3;
const DATA = 4;
const SOURCE = 5;
const API_SERVER = 'https://indrasnet.pythonanywhere.com/models/menu/';

class ActionMenu extends Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.state = {
      menu: {},
      loadingData: false,
      envFile: {},
      source: '',
      periodNum: 10,
      errorMessage: '',
      disabledButton: false,
      loadingSourceCode: false,
      loadingDebugger: false,
    };
  }
  // These two will go back in state above when graphs come back
  // loadingPopulation: false,
  // loadingScatter: false,

  async componentDidMount() {
    try {
      document.title = 'Indra | Menu';
      const m = await axios.get(API_SERVER);
      this.setState({
        menu: m.data,
        name: localStorage.getItem('name'),
        source: localStorage.getItem('source'),
        envFile: JSON.parse(localStorage.getItem('envFile')),
        msg: JSON.parse(localStorage.getItem('envFile')).user.user_msgs,
      });
    } catch (error) {
      return false;
    }
    // take graphs out for now!
    //    const defaultGraph = localStorage.getItem('graph');
    //    if (defaultGraph === 'scatter') {
    //      this.setState({
    //        loadingScatter: true,
    //      });
    //    } else {
    //      this.setState({
    //        loadingPopulation: true,
    //      });
    //    }
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

  // these next two lines go back in below when graphs go back in:
  //  loadingPopulation: false,
  //  loadingScatter: false,
  handleClick = (e) => {
    this.setState({
      loadingData: false,
      loadingSourceCode: false,
      loadingDebugger: false,
    });
    switch (e) {
      case POP:
        // this.setState({ loadingPopulation: true });
        break;
      case SCATTER:
        // this.setState({ loadingScatter: true });
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
    const { periodNum, envFile } = this.state;
    this.setState({ loadingData: true });
    try {
      const res = await axios.put(
        `${API_SERVER}run/${String(periodNum)}`,
        envFile,
        periodNum,
      );

      this.setState({
        envFile: res.data,
        loadingData: false,
        msg: res.data.user.user_msgs,
      });
      return true;
    } catch (e) {
      return false;
    }
  };

  renderHeader = () => {
    const { name } = this.state;
    return <h1 className="header">{name}</h1>;
  };

  MenuItem = (i, action, text, key) => (
    <ListGroup.Item
      className="w-50 text-primary p-3 list-group-item list-group-item-action"
      key={key}
      onClick={() => this.handleClick(action)}
    >
      {text}
    </ListGroup.Item>
  );

  renderMenuItem = () => {
    const {
      envFile,
      loadingDebugger,
      loadingSourceCode,
      sourceCode,
    } = this.state;
    return (
      <div>
        <Debugger loadingData={loadingDebugger} envFile={envFile} />
        <SourceCodeViewer loadingData={loadingSourceCode} code={sourceCode} />
      </div>
    );
  };
  // This stuff used to be returned above: graphs out for now!
  //        <PopulationGraph
  //          loadingData={loadingPopulation}
  //          envFile={envFile}
  //        />
  //
  //        <ScatterPlot
  //          loadingData={loadingScatter}
  //          envFile={envFile}
  //        />

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
      loadingData, msg, disabledButton, errorMessage,
    } = this.state;
    if (loadingData) {
      return <PageLoader />;
    }
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

ActionMenu.propTypes = {};

ActionMenu.defaultProps = {
  history: {},
};

export default ActionMenu;
