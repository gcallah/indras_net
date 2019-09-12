import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from 'axios';

class ModelDetail extends Component {
    api_server = 'https://indrasnet.pythonanywhere.com/models/props/';

    state = {
        model_details: {},
        loadingData: false,
        disabled_button: false,
        env_file:{},
    }

    async componentDidMount() {
        try{
            document.title = "Indra | Property";
            this.setState({ loadingData: true });
            console.log(this.api_server
                + `${localStorage.getItem("menu_id")}`)
            const properties = await axios.get(this.api_server
                + `${localStorage.getItem("menu_id")}`);
            this.setState({ model_details: properties.data });
            console.log(this.state.model_details)
            this.states(properties.data);
            this.errors(properties.data);
            this.setState({ loadingData: false });
        } catch(e) {
            console.log(e.message);
        }

    }


    states = data => {
        //loop over objects in data and create object in this.state
        Object.keys(this.state.model_details).forEach(item => 
            this.setState({[item]: data[item]})
        );
    }


    errors = data => {
        Object.keys(this.state.model_details).forEach(item => 
            this.setState(prevState => ({
                model_details: {
                    ...prevState.model_details,          
                    [item]:{                     
                    ...prevState.model_details[item],  
                    errorMessage: '' ,
                    disabledButton: false,       
                    } 
                }
            })
        ))
    }


    errorSubmit = () =>{
        let ans = false
        Object.keys(this.state.model_details).forEach(item => 
            ans = ans || this.state.model_details[item]['disabledButton'])
        return ans
    }

    propChanged = e =>{ 
        let model_detail = this.state.model_details;
        const {name,value} = e.target
        let valid = this.checkValidity(name,value)
        model_detail[name]['disabledButton']=true

        if (valid === 1) {
            model_detail[name]['val']= value
            model_detail[name]['errorMessage']=""
            model_detail[name]['disabledButton']=false
            this.setState({model_details:model_detail})

        } else if(valid === -1) {
            model_detail[name]['errorMessage']="**Wrong Input Type"
            model_detail[name]['val']= this.state[name]['val']
            this.setState({model_details:model_detail})
            console.log(this.state.model_details[name])

        } else {
            model_detail[name]['errorMessage'] 
                = `**Please input a number between ${this.state[name]['lowval']} and ${this.state[name]['hival']}.`
            model_detail[name]['val'] = this.state[name]['val']
            this.setState({model_details:model_detail})
        }  

        this.setState({disabled_button: this.errorSubmit()}) 
    }


    checkValidity = (name,value) => {
        if (value <= this.state.model_details[name]['hival']
                && value >= this.state.model_details[name]['lowval']){
            if (this.state.model_details[name]['atype'] === 'INT'
                && !!(value%1) === false) {
                return 1
            }
            else if(this.state.model_details[name]['atype'] === 'DBL'){
                return 1
            }
            else {
                return -1
            }
        }
        else return 0
    }


    handleSubmit = async() => {
        event.preventDefault();
        console.log(this.state.model_details)
        try{
            const res = await axios.put(this.api_server + localStorage.getItem("menu_id"), this.state.model_details)
            var item_id = localStorage.getItem("menu_id")
            this.setState({env_file: res.data})
            localStorage.setItem("env_file", JSON.stringify(this.state.env_file))
            this.props.history.push({pathname:"/models/menu/" + (item_id.toString(10)) ,state: {
            env_file: this.state.env_file,
            }});
        }
        catch(e){
            console.log(e.message)
            this.props.history.push('/errorCatching')
        }
    }

    renderHeader = () => {
        return <h1 style={{ "textAlign": "center", "fontWeight": '200' }}>Please set the parameters for the {localStorage.getItem("name")} model</h1>
    }

    renderSubmitButton = () => {
        const { disabled_button } = this.state;
        return <button disabled={disabled_button} onClick={!disabled_button ? this.handleSubmit : null}
        className="btn btn-primary m-2">Submit</button>
    }

    goback=()=>{
        this.props.history.goBack();
    }

    renderDimmer = () => {
        return (
            <Dimmer active inverted>
            <Loader size='massive'>Loading...</Loader>
            </Dimmer>
        );
    }


    render() {

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
                <br />
                {this.renderHeader()}
                <br /><br />
                <form>
                    <div className="container">
                    {Object.keys(this.state.model_details).map((item,i)=> {
                        if ('question' in this.state.model_details[item]){
                            return(
                            <div className="form-group">
                                <div>
                                    <label className="col-sm-4 col-md-4 col-lg-4"
                                        key={i}>{this.state.model_details[item]['question']} {" "}
                                    </label>
                                    <input type={this.state.model_details[item]['atype']}
                                    className="col-sm-2 col-md-2 col-lg-2" style={{fontSize:"15pt"}}
                                    placeholder={this.state.model_details[item]['val']}
                                    onChange={this.propChanged} /*style={{width: 60}} */ name={item}/>
                                    <span className="col-sm-6 col-md-6 col-lg-6" style={{color:"red", fontSize: 12}}>
                                    {this.state.model_details[item]['errorMessage']}</span>
                                    <br/>
                                </div>
                            </div>
                            )}
                        })
                    }
                    </div>
                </form>
                <br /><br />
                {this.renderSubmitButton()}
            </div>
        );
    }
}

export default ModelDetail;
