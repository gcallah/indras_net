import React, {Component} from 'react';

function renderPreFormTextBox(props){
	return(
      <div class="card w-50 overflow-auto" style={{float:'right', width:"18rem", height:"18rem"}}>
      <h5 style={{textAlign: 'center', "fontSize": 16}}
          class="card-header bg-primary text-white">{"Model Status"}</h5>
      <div class="card-body">
      <pre>
      {props.msg}
      </pre>
      </div>
      </div>
	)
}

export default renderPreFormTextBox;
