/* eslint-disable react/prop-types */
/* eslint-disable react/destructuring-assignment */
import React from 'react';
import autoBind from 'react-autobind';

export default class ModelStatusBox extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.state = {
      msg: this.props.msg,
      title: this.props.title,
    };
  }

  // componentWillReceiveProps(nextProps) {
  //   if (nextProps.msg !== '') {
  //     this.setState({ msg: nextProps.msg });
  //   }
  // }

  static getDerivedStateFromProps(nextProps, prevState) {
    if (nextProps.msg !== prevState.msg) {
      return { msg: nextProps.msg };
    }
    return null;
  }

  render() {
    return (
      <div>
        <div className="card w-50 model-status">
          <h5
            style={{ textAlign: 'center', fontSize: 16 }}
            className="card-header bg-primary text-white"
          >
            { this.state.title }
          </h5>
          <div className="card-body overflow-auto">
            <pre className="card-text">
              { this.state.msg }
            </pre>
          </div>
        </div>
      </div>
    );
  }
}
