import React from 'react';
import { LineChart } from 'react-chartkick';
import 'chart.js';
import PropType from 'prop-types';

const FMARKET = 5;

function PopulationGraph(props) {
  const { loadingData } = props;
  if (loadingData) {
    const data = [];
    if (props.id !== FMARKET) {
      const env = props.envFile.pop_hist.pops;
      // populate 'data' array with groups from 'pops' and their respective values
      Object.keys(env).forEach((group, iGroup) => {
        data.push({
          name: group,
          color: props.envFile.members[group].attrs.color,
          data: {},
        });
        // modify individual 'data' dictionary of each pops group by copying over value
        Object.keys(env[group]).forEach((member, iMember) => {
          data[iGroup].data[member] = env[group][iMember];
        });
      });
    } else {
      const period = props.envFile.pop_hist.periods;
      const dataHist = props.envFile.members.market_maker.attrs.price_hist;
      let i;
      data.push({ name: 'price history', data: {} });
      for (i = 0; i < period; i += 1) {
        data[0].data[i] = dataHist[i];
      }
    }
    return (
      <div>
        <LineChart data={data} width="600px" height="600px" />
      </div>
    );
  }
  return null;
}

PopulationGraph.propTypes = {
  loadingData: PropType.bool,
  id: PropType.number,
  envFile: PropType.shape(),
};

PopulationGraph.defaultProps = {
  loadingData: true,
  id: 0,
  envFile: {},
};

export default PopulationGraph;
