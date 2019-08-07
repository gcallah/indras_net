import React from "react";
import { ScatterChart } from 'react-chartkick'
import 'chart.js'

function ScatterPlot(props) {
    if (props.loadingData){
        let env=props.env_file['members']
        let WIDTH=props.env_file['props']['grid_height']['val']
        let HEIGHT=props.env_file['props']['grid_width']['val']
        console.log(HEIGHT)
        console.log(WIDTH)
        console.log(env)
        var data=[]
        Object.keys(env).map((group,i_group)=> {
            return(
                data.push({name:env[group]['name'],color: env[group]['attrs']['color'], data: []}),
                Object.keys(env[group]['members']).map((member, i_member)=>{
                    return(
                        data[i_group]['data'].push(env[group]['members'][member]['pos'])
                    )
                })
            )
        });
        console.log(data)
        return (
            <div>
                <ScatterChart style={{flex:1, alignItems:'center', margin:'auto'}}
                    data={data} width='600px' height='600px'/>
            </div>
        );
    }
    else{
        return(null)
}};


export default ScatterPlot;
