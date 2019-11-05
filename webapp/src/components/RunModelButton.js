import React from 'react';
import autoBind from 'react-autobind';

export default class RunModelButton extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);
    this.state = {
      disabledButton: this.props.disabledButton,
      errorMessage: this.props.errorMessage
    };
  }
  render() {
    return (
      <div>
        <button
          type="button"
          disabled={this.state.disabledButton}
          onClick={!this.state.disabledButton ? this.props.sendNumPeriods : null}
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
          onChange={this.props.handleRunPeriod}
        />
        {' '}
        periods.
        <span className="error-message">
          {this.state.errorMessage}
        </span>
      </div>
    );
  }
}