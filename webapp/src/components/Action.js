import React from "react";

function Action(props) {
  var imageName = require('./images/forestfire.png')
  if (props.loadingData){
  return (
    <div>
      <br /><br />
      
      <p align='center'>We are updating the model! The figure like this will be displayed soon!</p>
      <img alt="" style={{display:'block', marginLeft:'auto', marginRight:'auto'}}src={imageName} align="middle"/>

      <br /><br />
    </div>
    );
  }else{
    return(null)
  }}


export default Action;
