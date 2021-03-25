import React from 'react';
import { ColumnChart } from 'react-chartkick';
import 'chart.js';
import PropType from 'prop-types';
import CardWrapper from './CardWrapper';

function PopulationBarGraph(props) {
  const NUM_COLORS = 7;
  const colors = [
    'red',
    'green',
    'blue',
    'black',
    'purple',
    'magenta',
    'orange',
  ];
  let thisColor = 0;
  let dataset = [];
  const { loadingData, envFile } = props;
  if (loadingData) {
    const data = [];
    const env = props.envFile.pop_hist.pops;
    // populate 'data' array with groups from 'pops'
    // and their respective values
    Object.keys(env).forEach((group, iGroup) => {
      data.push({
        name: group,
        // color: colors[thisColor % NUM_COLORS],
        color: envFile.members[group]
          ? envFile.members[group].attrs.color
          : colors[thisColor % NUM_COLORS],
        data: {},
      });
      // modify individual 'data' dictionary of each pops
      // group by copying over value
      Object.keys(env[group]).forEach((member, iMember) => {
        data[iGroup].data[member] = env[group][iMember];
      });
      thisColor += 1;
      dataset = data.map((datum) => {
        const totalSum = Object.keys(datum.data)
          .map((key) => datum.data[key])
          .reduce((prev, curr) => prev + curr, 0);
        return [datum.name, totalSum];
      });
    });
    return (
      <CardWrapper title="Population Bar Graph">
        <ColumnChart data={dataset} width="600px" height="600px" />
      </CardWrapper>
    );
  }
  return null;
}

PopulationBarGraph.propTypes = {
  loadingData: PropType.bool,
  envFile: PropType.shape(),
};

PopulationBarGraph.defaultProps = {
  loadingData: true,
  envFile: {},
};

export default PopulationBarGraph;
