import React from 'react';
import PropTypes from 'prop-types';
import CardWrapper from './CardWrapper';

const LogsViewer = ({ loadingData, envFile }) => {
  if (!loadingData) return null;
  return (
    <CardWrapper title="Logs">
      <div style={{ whiteSpace: 'pre-line' }}>
        {envFile.user.debug || 'Run the model to see the logs'}
      </div>
    </CardWrapper>
  );
};

LogsViewer.propTypes = {
  loadingData: PropTypes.bool,
  envFile: PropTypes.shape(),
};

LogsViewer.defaultProps = {
  loadingData: true,
  envFile: {},
};

export default LogsViewer;
