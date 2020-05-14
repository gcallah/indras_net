import React from 'react';
import autoBind from 'react-autobind';
import PropTypes from 'prop-types';

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
    const {
      disabledButton, sendNumPeriods, handleRunPeriod, errorMessage,
    } = this.state;
    return (
      <div>
        <button
          type="button"
          disabled={disabledButton}
          onClick={!disabledButton ? sendNumPeriods : null}
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
          style={{ width: '40px' }}
          placeholder="10"
          onChange={handleRunPeriod}
        />
        {' '}
        periods.
        <span className="error-message">
          {errorMessage}
        </span>
      </div>
    );
  }
}

RunModelButton.propTypes = {
  disabledButton: PropTypes.bool,
  errorMessage: PropTypes.string,
  sendNumPeriods: PropTypes.func,
  handleRunPeriod: PropTypes.func,
};

RunModelButton.defaultProps = {
  disabledButton: true,
  errorMessage: '',
  sendNumPeriods() {},
  handleRunPeriod() {},
};
