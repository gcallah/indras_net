import React from "react";
import { LineChart } from "react-chartkick";
import "chart.js";

const FMARKET = 5;

function PopulationGraph(props) {
  if (props.loadingData) {
    var data = [];
    console.log("props.id = " + props.id);
    if (props.id !== FMARKET) {
      let env = props.env_file["pop_hist"]["pops"];
      Object.keys(env).map((group, i_group) => {
        console.log(props.env_file["members"][group]["attrs"]["color"]);
        /*
         * Must determine what this code does and write it more clearly
         * if possible.
         */
        return (
          data.push({
            name: group,
            color: props.env_file["members"][group]["attrs"]["color"],
            data: {}
          }),
          Object.keys(env[group]).map((member, i_member) => {
            console.log(member);
            return (data[i_group]["data"][member] = env[group][i_member]);
          })
        );
      });
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
    console.log("data passed to line graph", data);
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
