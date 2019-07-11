import React from "react";

function PopulationGraph(props) {
  var imageName = require('./images/wolfsheep_population_graph.png')
  if (props.loadingData){
    console.log("inside PopulationGraph")
  return (
    <div>
      <br /><br />
      
      <p align='center'>We are updating the model! The figure like this will be displayed soon!</p>
      <img alt="" style={{display:'block', marginLeft:'auto', marginRight:'auto', width:'50%'}} src={imageName} align="middle"/>

      <br /><br />
    </div>
    );
  }else{
    return(null)
  }}

export default PopulationGraph;
