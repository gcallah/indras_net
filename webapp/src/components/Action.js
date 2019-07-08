import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";

function Action(props) {
  var imageName = require('./images/forestfire.png')
  if (props.loadingData){
  return (
    <div>
      <br />
      <h2 style={{ "textAlign": "center" }}>Welcome to the Indra ABM platform!
      </h2>
      <br /><br />
      
      <p>We are updating the model! The figure like this will be displayed soon!</p>
      <img src={imageName} />

      <br /><br />
    </div>
    );
  }else{
    return(null)
  }}


export default Action;
