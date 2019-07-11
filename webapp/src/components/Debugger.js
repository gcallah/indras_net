import React from "react";
import Tree from 'react-tree-graph';
import { easeElastic } from 'd3-ease';
import 'react-tree-graph/dist/style.css'
import ReactJson from 'react-json-view'

function onClick(event, nodeKey) {
  alert(nodeKey);
}


function Debugger(props){
  let data = props.env_file
  console.log(data)
  if (props.loadingData){
    console.log("inside Debugger")
    return(
      <ReactJson src={data} />
    )
  }
  else {
    return (null)
  }
}

export default Debugger;