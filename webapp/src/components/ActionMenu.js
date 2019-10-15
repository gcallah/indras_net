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
const API_SERVER = 'https://indrasnet.pythonanywhere.com/models/menu/';

class ActionMenu extends Component {

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
        document.title = 'Indra | Menu';
        const m = await axios.get (API_SERVER);
        console.log (API_SERVER);
        this.setState ({
            menu: m.data,
            name: localStorage.getItem ('name'),
            model_id: localStorage.getItem ('menu_id'),
            source: localStorage.getItem ('source'),
            env_file: JSON.parse(localStorage.getItem('env_file')),
            msg: JSON.parse(localStorage.getItem('env_file'))["user"]["user_msgs"]
        });
        console.log(this.state)
    }

    viewSource = () => {
        var source = localStorage.getItem ('source');
        window.open (source);
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
            this.setState ({
                errorMessage: '**Please input an integer',
                disabled_button: true
            });
        } else {
            this.setState ({
                errorMessage: '',
                disabled_button: false
            });
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
        this.setState ({
            loadingData: false,
            loading_population: false,
            loading_scatter: false,
            loading_debugger: false,
            action_id: e
        })
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
        console.log(API_SERVER + 'run/' + String(this.state.period_num))
        this.setState({loadingData:true})
        try { 
            const res = await axios.put(
            API_SERVER + 'run/' + String(this.state.period_num),
            this.state.env_file,
            this.state.period_num
        )

        this.setState({env_file: res.data,
                            loadingData:false,
                            msg: res.data["user"]["user_msgs"]})
        console.log(res.data)
        } catch(e) {
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
        <a className="w-50 p-3 list-group-item list-group-item-action" key={i}>
            <Link className="text-primary"
                onClick={() => this.handleClick(action)}>
                { text }
            </Link>
        </a>
        );
    }

    renderModelStatus = () => {
        return (
            <div>
                <div className="card w-50 overflow-auto"
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

    renderMenuItem = () => {
        return (
            <div>
                <PopulationGraph
                loadingData={this.state.loading_population}
                env_file={this.state.env_file}
                id={this.state.model_id}
                />

                <ScatterPlot
                loadingData={this.state.loading_scatter}
                env_file={this.state.env_file}
                id={this.state.model_id}
                />

                <Debugger
                loadingData={this.state.loading_debugger}
                env_file={this.state.env_file}
                />
            </div>
        )
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
                        className="from-control m-2"
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

    renderMapItem = () => {
        return (
            <div className="row">
                <div className="col">
                {
                    Object.keys (this.state.menu).map ((item, i) => (
                        <div key={i}>
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
        )
    }
    
    render () {
        if (this.state.loadingData) {
            return (
                <div className="container-fluid" style={{height:600}}>
                    <div className="row text-center" style={{height:'100%'}} >
                        <div className="col-12" style={{display: "flex",justifyContent: "center", alignItems: "center"}}>
                            <div className="spinner-border" role="status">
                                <span className="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
        else {
            return (
                <div>
                    <br/>
                    {this.renderHeader()}
                    <br/><br/>
                    {this.renderModelStatus()}
                    <ul className="list-group">
                        <div className="row">
                            <div>
                                {this.renderRunButton()}
                                <br/><br/>
                                <h3>Model Analysis:</h3>
                                <br/>
                            </div>
                        </div>
                        {this.renderMapItem()}
                    </ul>
                    <br/><br/>
                    <br/><br/>
                    {this.renderMenuItem()}
                </div>
            );
        }
    }

}

export default ActionMenu;
