/* eslint-disable no-plusplus */
/* eslint-disable no-return-assign */
/* eslint-disable implicit-arrow-linebreak */
/* eslint-disable camelcase */
/* eslint-disable react/prop-types */
/* eslint-disable react/destructuring-assignment */
import React from 'react';
import { LineChart } from 'react-chartkick';
import 'chart.js';

const FMARKET = 5;

function PopulationGraph(props) {
  if (props.loadingData) {
    const data = [];
    if (props.id !== FMARKET) {
      const env = props.envFile.pop_hist.pops;
      // populate 'data' array with groups from 'pops' and their respective values
      Object.keys(env).forEach((group, i_group) => {
        data.push({
          name: group,
          color: props.envFile.members[group].attrs.color,
          data: {},
        });
        // modify individual 'data' dictionary of each pops group by copying over value
        Object.keys(env[group]).forEach((member, i_member) => {
          data[i_group].data[member] = env[group][i_member];
        });
      });
    } else {
      const period = props.envFile.pop_hist.periods;
      const data_hist = props.envFile.members.market_maker.attrs.price_hist;
      let i;
      data.push({ name: 'price history', data: {} });
      for (i = 0; i < period; i++) {
        data[0].data[i] = data_hist[i];
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

export default PopulationGraph;
