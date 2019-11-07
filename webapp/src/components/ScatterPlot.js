/* eslint-disable no-console */
/* eslint-disable no-unused-vars */
/* eslint-disable camelcase */
/* eslint-disable react/prop-types */
import React from 'react';
import { ScatterChart } from 'react-chartkick';
import 'chart.js';

const FMARKET = 10;
function ScatterPlot(props) {
  const { loadingData, envFile, id } = props;
  if (loadingData && id !== FMARKET) {
    const env = envFile.members;
    const WIDTH = envFile.props.grid_height.val;
    const HEIGHT = envFile.props.grid_width.val;
    console.log(HEIGHT);
    console.log(WIDTH);
    console.log(env);
    const data = [];
    Object.keys(env).forEach((group, i_group) => {
      data.push({
        name: env[group].name,
        color: env[group].attrs.color,
        data: [],
      });
      Object.keys(env[group].members).forEach((member, i_member) => {
        if (env[group].members[member].pos !== null) {
          data[i_group].data.push(
            env[group].members[member].pos,
          );
        }
      });
    });
    console.log(data);
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
  if (loadingData && id === FMARKET) {
    return <p> There is no scatter plot available for this model! </p>;
  }
  return null;
}

export default ScatterPlot;
