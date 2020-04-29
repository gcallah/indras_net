import React from 'react';
import { LineChart } from 'react-chartkick';
import 'chart.js';
import PropType from 'prop-types';
import CardWrapper from './CardWrapper';

function PopulationGraph(props) {
  const { loadingData } = props;
  if (loadingData) {
    const data = [];
    const env = props.envFile.pop_hist.pops;
    // populate 'data' array with groups from 'pops'
    // and their respective values
    Object.keys(env).forEach((group, iGroup) => {
      data.push({
        name: group,
        color: props.envFile.members[group].attrs.color,
        data: {},
      });
      // modify individual 'data' dictionary of each pops
      // group by copying over value
      Object.keys(env[group]).forEach((member, iMember) => {
        data[iGroup].data[member] = env[group][iMember];
      });
    });
    return (
      <CardWrapper title="Population Graph">
        <LineChart data={data} width="600px" height="600px" />
      </CardWrapper>
    );
  }
  return null;
}

PopulationGraph.propTypes = {
  loadingData: PropType.bool,
  envFile: PropType.shape(),
};

PopulationGraph.defaultProps = {
  loadingData: true,
  envFile: {},
};

export default PopulationGraph;
