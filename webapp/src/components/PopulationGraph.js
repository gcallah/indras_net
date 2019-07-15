import React from "react";
import { LineChart } from 'react-chartkick'
import 'chart.js'

function PopulationGraph(props) {
  if (props.loadingData){
    let env=props.env_file['pop_hist']['pops']
    let WIDTH=props.env_file['props']['grid_height']['val']
    let HEIGHT=props.env_file['props']['grid_width']['val']
    console.log(HEIGHT)
    console.log(WIDTH)
    console.log(env)
    var data=[]
    Object.keys(env).map((group,i_group)=> {
      console.log(props.env_file['members'][group]['attrs']['color'])
      return(
        data.push({name:group,color: props.env_file['members'][group]['attrs']['color'], data: {}}),
        Object.keys(env[group]).map((member, i_member)=>{
          console.log(member)
          return(
            data[i_group]['data'][member] = env[group][i_member]
          )
        })
      )
    });
    console.log(data)
    return (
      <div>
          <LineChart
            data={data} width='600px' height='600px'
          />
      </div>
    );
  }
  else{
    return(null)
  }};

export default PopulationGraph;

