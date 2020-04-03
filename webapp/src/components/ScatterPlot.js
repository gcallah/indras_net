/* eslint-disable no-unused-vars */
import React from 'react';
import { ScatterChart } from 'react-chartkick';
import 'chart.js';
import PropTypes from 'prop-types';

function ScatterPlot(props) {
  const { loadingData, envFile, id } = props;
  if (loadingData) {
    const env = envFile.members;
    const data = [];
    Object.keys(env).forEach((group, iGroup) => {
      data.push({
        name: env[group].name,
        color: env[group].attrs.color,
        data: [],
      });
      Object.keys(env[group].members).forEach((member) => {
        if (env[group].members[member].pos !== null) {
          data[iGroup].data.push(
            env[group].members[member].pos,
          );
        }
      });
    });
    return (
      <div>
        <ScatterChart
          data={data}
          width="600px"
          height="600px"
        />
      </div>
    );
  }
  return null;
}

ScatterPlot.propTypes = {
  loadingData: PropTypes.bool,
  envFile: PropTypes.shape(),
  id: PropTypes.number,
};

ScatterPlot.defaultProps = {
  loadingData: true,
  envFile: {},
  id: 0,
};

export default ScatterPlot;
