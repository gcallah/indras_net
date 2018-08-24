#!/usr/bin/env python3
"""
Set up and run the auditorium model.
"""
MODEL_NM = "auditorium"

import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import schelling.auditorium as am

# set up some file names:


def run(prop_dict=None):
    (prog_file, log_file, 
     prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    global pa

    # Now we create an environment for our agents to act within:
    env = am.Auditorium("Auditorium",
                        height=pa["grid_height"],
                        width=pa["grid_width"],
                        torus=False,
                        model_nm=MODEL_NM,
                        num_agents=pa["num_agents"],
                        props=pa)
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
