import React from 'react';
import autoBind from 'react-autobind';
export default class ModelStatusBox extends React.Component {
  constructor(props) {
        super(props);
        autoBind(this);
        this.state = {
            msg:this.props.msg,
            title:this.props.title
        };
    }
  componentWillReceiveProps(nextProps){
    console.log("inside  modelbox ", this.state.msg);
    console.log('component will receive props', nextProps);
    if(nextProps.msg!==""){
      this.setState({msg:nextProps.msg});
    }
  }
  
  render() {
    
    return (
        <div>
        <h5 style={{textAlign: 'center', "fontSize": 16}}className="card-header bg-primary text-white">
        { this.state.title }
        </h5>
        <div className="card-body">
        {this.state.msg}
        </div>
    </div>
    );
  }
}