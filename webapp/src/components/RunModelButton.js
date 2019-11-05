/* eslint-disable react/prop-types */
/* eslint-disable react/destructuring-assignment */
/* eslint no-trailing-spaces: "error" */
import React from 'react';
import autoBind from 'react-autobind';

export default class RunModelButton extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);

    this.state = {
      disabledButton: props.disabledButton,
      errorMessage: props.errorMessage,
      sendNumPeriods: props.sendNumPeriods,
      handleRunPeriod: props.handleRunPeriod,
    };
  }

  render() {
    return (
      <div>
        <button
          type="button"
          disabled={this.state.disabledButton}
          onClick={!this.state.disabledButton ? this.state.sendNumPeriods : null}
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
          onChange={this.state.handleRunPeriod}
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
