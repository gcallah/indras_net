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

  render() {
    return (
        <div>
        <h5 style={{textAlign: 'center', "fontSize": 16}}className="card-header bg-primary text-white">
        { this.state.title }
        </h5>
        <div className="card-body">
        <p class="card-text">
        {this.state.msg}
        </p>
        </div>
    </div>
    );
  }
}