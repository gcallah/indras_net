/* eslint-disable react/prop-types */
import React from 'react';
import ReactJson from 'react-json-view';


function Debugger(props) {
  const { envFile, loadingData } = props;
  const data = envFile;
  console.log(data);
  if (loadingData) {
    console.log('inside Debugger');
    return (
      <ReactJson src={data} />
    );
  }
  return (null);
}

export default Debugger;
