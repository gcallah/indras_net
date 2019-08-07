import React, {Component} from 'react';
import {Loader, Dimmer } from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import axios from 'axios';
import PopulationGraph from './PopulationGraph.js';
import ScatterPlot from './ScatterPlot.js';
import Debugger from './Debugger.js';
import PreFormTextBox from './PreFormTextBox.js';

const POP = 2;
const SCATTER = 3;
const DATA = 4;
const SOURCE = 5;


class ActionMenu extends Component {
  api_server = 'https://indrasnet.pythonanywhere.com/models/menu/';

  state = {
    msg: '',
    menu: {},
    loadingData: false,
    env_file: {},
    model_id: 0,
    action_id: 0,
    show_component: false,
    period_num: 10,
    errorMessage: '',
    disabled_button: false,
    loading_population: false,
    loading_scatter: false,
    loading_debugger: false,
  };

  async componentDidMount () {
    this.setState ({loadingData: true});
    document.title = 'Indra | Menu';
    const m = await axios.get (this.api_server);
    console.log (this.api_server);
    this.setState ({menu: m.data});
    const id = localStorage.getItem ('menu_id');
    const name = localStorage.getItem ('name');
    const source = localStorage.getItem ('source');
    const env = localStorage.getItem('env_file')
    this.setState ({name: name});
    this.setState ({model_id: id});
    this.setState ({source: source});
    this.setState ({loadingData: false});
    this.setState ({env_file: JSON.parse(env)});
    this.setState({msg: this.state.env_file["user"]["user_msgs"]})
  }

  viewSource = () => {
    var source = localStorage.getItem ('source');
    window.open (source);
  };

  goback = () => {
    this.props.history.replace ({
      pathname: '/models/props/',
      state: {
        menu_id: localStorage.getItem ('menu_id'),
        name: localStorage.getItem ('name'),
      },
    });
  };

  onClick = () => {
    this.setState ({
      show_component: true,
    });
  };

  handleRunPeriod = e => {
    this.setState ({
      period_num: e.target.value,
    });

    let valid = this.checkValidity (e.target.value);
    if (valid === 0) {
      this.setState ({errorMessage: '**Please input an integer'});
      this.setState ({disabled_button: true});
    } else {
      this.setState ({errorMessage: ''});
      this.setState ({disabled_button: false});
    }
  };

  checkValidity = data => {
    let remainder = data % 1;
    if (remainder === 0) {
      return 1;
    } else return 0;
  };

  handleClick = e => {
      console.log("e = " + String(e))
    this.setState ({loadingData: false});
    this.setState ({loading_population: false});
    this.setState ({loading_scatter: false});
    this.setState ({action_id: e});
    switch (e) {
        case POP:
            this.setState ({loading_population: true});
            break;
        case SCATTER:
            this.setState ({loading_scatter: true});
            break;
        case DATA:
            this.setState ({loading_debugger: true});
            break;
        case SOURCE:
            this.viewSource ();
            break;
        default:
            break;
    }
  };

  sendNumPeriods = async() => {
    console.log(this.api_server + 'run/' + String(this.state.period_num))
    try{
      const res = await axios.put(
      this.api_server + 'run/' + String(this.state.period_num),
      this.state.env_file,
      this.state.period_num
      )
      this.setState({env_file: res.data})
      this.setState({msg: res.data["user"]["user_msgs"]})
      console.log(res.data)
    }catch(e){
      console.log(e.message)
    }

  };

  renderHeader = () => {
    return <h1 style={{textAlign: 'center', fontWeight: '200'}}>
    {this.state.name}
    </h1>
  }


  MenuItem = (i, action, text) => {
      return (
          <a class="w-50 p-3 list-group-item list-group-item-action" key={i}>
          <Link class="text-primary"
              onClick={() => this.handleClick(action)}
          >
          { text }
          </Link>
          </a>
      );
  }

  renderModelStatus = () => {
     return (
        <div>
        <div class="card w-50 overflow-auto"
            style={{float:'right', width:"18rem", height:"18rem"}}>
            { PreFormTextBox("Model Status", this.state.msg) } 
        </div>
        </div>
        );
    }

    renderDimmer = () => {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading...</Loader>
        </Dimmer>
      );
    }

  renderRunButton = () => {
      return (
          <div>
        <button 
          disabled={this.state.disabled_button}
          onClick={
            !this.state.disabled_button ? this.sendNumPeriods : null
          }
          className="btn btn-success m-2"
        >
          {'  '}Run{'  '}
        </button>
        {' '}
        <span>model for</span>
        {' '}
        <input
          style={{width: 30, height: 30}}
          type="INT"
          class="from-control m-2"
          placeholder="10"
          onChange={this.handleRunPeriod}
        />
        {' '}
        periods.
        <span style={{color: 'red', fontSize: 12}}>
          {this.state.errorMessage}
        </span>
          </div>
      );
  }

  render () {
    if (this.state.loadingData) {
      return (
        <div>
        {this.renderDimmer()}
        </div>
      );
    }
    return (
      <div>
        <br />
        {this.renderHeader()}
        <br /><br />
        { this.renderModelStatus() }
          <ul class="list-group">
            <div class="row">
              <div>
                { this.renderRunButton() }
                <br /><br />
                <h3>Model Analysis:</h3>
                <br />
              </div>
            </div>
            <div class="row">
              <div class="col">
              {
              Object.keys (this.state.menu).map ((item, i) => (
              <div>
              {
                  this.state.menu[item]['id'] > 1 ?
                      this.MenuItem(i,
                                    this.state.menu[item]['id'],
                                    this.state.menu[item]['question'])
                  : null
              }
              </div>

              )
            )
          }
        </div>
        </div>
        </ul>
        <br /><br />
        <br /><br />

        <PopulationGraph
          loadingData={this.state.loading_population}
          env_file={this.state.env_file}
        />

        <ScatterPlot
          loadingData={this.state.loading_scatter}
          env_file={this.state.env_file}
        />

        <Debugger
          loadingData={this.state.loading_debugger}
          env_file={this.state.env_file}
        />

      </div>
    );
  }
}

export default ActionMenu;
