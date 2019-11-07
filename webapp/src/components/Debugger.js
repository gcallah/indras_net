import React from 'react';
import ReactJson from 'react-json-view';
import propTypes from 'prop-types';


function Debugger(props) {
  const { envFile, loadingData } = props;
  const data = envFile;
  if (loadingData) {
    return (
      <ReactJson src={data} />
    );
  }
  return (null);
}

Debugger.propTypes = {
  envFile: propTypes.shape(),
  loadingData: propTypes.bool,
};

Debugger.defaultProps = {
  envFile: {},
  loadingData: true,
};

export default Debugger;
