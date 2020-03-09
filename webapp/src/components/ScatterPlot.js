/* eslint-disable no-unused-vars */
import React from "react";
import { ScatterChart } from "react-chartkick";
import "chart.js";
import PropTypes from "prop-types";

const FMARKET = 10;
function ScatterPlot(props) {
  const { loadingData, envFile, id } = props;
  if (loadingData && id !== FMARKET) {
    const env = envFile.members;
    // TODO: width and height are set but never used
    // const WIDTH = envFile.props.grid_height.val;
    // const HEIGHT = envFile.props.grid_width.val;
    const data = [];
    Object.keys(env).forEach((group, iGroup) => {
      data.push({
        name: env[group].name,
        color: env[group].attrs.color,
        data: []
      });
      Object.keys(env[group].members).forEach(member => {
        if (env[group].members[member].pos !== null) {
          data[iGroup].data.push(env[group].members[member].pos);
        }
      });
    });
    return (
      <div>
        <ScatterChart data={data} width="600px" height="600px" />
      </div>
    );
  }
  if (loadingData && id === FMARKET) {
    return <p> There is no scatter plot available for this model! </p>;
  }
  return null;
}

ScatterPlot.propTypes = {
  loadingData: PropTypes.bool,
  envFile: PropTypes.shape(),
  id: PropTypes.number
};

ScatterPlot.defaultProps = {
  loadingData: true,
  envFile: {},
  id: 0
};

export default ScatterPlot;
