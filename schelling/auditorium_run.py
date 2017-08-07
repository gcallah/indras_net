#!/usr/bin/env python3
"""
Set up and run the auditorium model.
"""

import indra.utils as utils
import indra.prop_args as props
import schelling.auditorium_model as am

# set up some file names:
MODEL_NM = "auditorium_model"

def run():
    (prog_file, log_file, 
     prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_grid_dims(pa, 8)
        utils.get_agent_num(pa, "num_agents", "agents", 16)
    
    # Now we create a minimal environment for our agents to act within:
    env = am.Auditorium("Auditorium",
                        height=pa.get("grid_height"),
                        width=pa.get("grid_width"),
                        torus=False,
                        model_nm=MODEL_NM,
                        num_agents=pa.get("num_agents"),
                        props=pa)
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
