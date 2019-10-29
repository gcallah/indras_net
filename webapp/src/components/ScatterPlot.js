import React from 'react';
import { ScatterChart } from 'react-chartkick';
import 'chart.js';

const FMARKET = 10;
function ScatterPlot(props) {
  const {loadingData, env_file, id} = props;
  if (loadingData && id !== FMARKET) {
    const env = env_file.members;
    const WIDTH = env_file.props.grid_height.val;
    const HEIGHT = env_file.props.grid_width.val;
    console.log(HEIGHT);
    console.log(WIDTH);
    console.log(env);
    const data = [];
    Object.keys(env).map((group, i_group) => {
      return (
        data.push({
          name: env[group].name,
          color: env[group].attrs.color,
          data: [],
        }),
        Object.keys(env[group].members).map((member, i_member) => {
          if (env[group].members[member].pos !== null) {
            return data[i_group].data.push(
              env[group].members[member].pos,
            );
          } 
        })
      );
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
