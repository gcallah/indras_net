import React from 'react';
import ReactJson from 'react-json-view';
import propTypes from 'prop-types';
import CardWrapper from './CardWrapper';

function Debugger(props) {
  const { envFile, loadingData } = props;
  const data = envFile;
  if (loadingData) {
    return (
      <CardWrapper title="Model Data">
        <ReactJson src={data} />
      </CardWrapper>
    );
  }
  return null;
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
