import React from "react";
import { LineChart } from "react-chartkick";
import "chart.js";

const FMARKET = 5;

function PopulationGraph(props) {
  if (props.loadingData) {
    var data = [];
    // if not Financial Market
    if (props.id !== FMARKET) {
      // ["pop_hist"]["pops"] == group == agent name
      let env = props.env_file["pop_hist"]["pops"];
      Object.keys(env).map((group, i_group) => {
        // populate 'data' array with members of 'pops' with their respective values
        return (
          data.push({
            name: group,
            color: props.env_file["members"][group]["attrs"]["color"],
            data: {}
          }),
          // modify 'data' dictionary of each pops member by copying 'pops' data
          Object.keys(env[group]).map((member, i_member) => {
            return (data[i_group]["data"][member] = env[group][i_member]);
          })
        );
      });
    // if Financial Market
    } else {
      let period = props.env_file["pop_hist"]["periods"];
      let data_hist =
        props.env_file["members"]["market_maker"]["attrs"]["price_hist"];
      var i;
      data.push({ name: "price history", data: {} });
      for (i = 0; i < period; i++) {
        data[0]["data"][i] = data_hist[i];
      }
    }
    return (
      <div>
        <LineChart data={data} width="600px" height="600px" />
      </div>
    );
  } else {
    return null;
  }
}

export default PopulationGraph;
