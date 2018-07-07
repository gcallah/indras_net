#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""
MODEL_NM = "Wolfram"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.prop_args as props
import wolfram.wolfram_model as wm

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    global pa

    if prop_dict is not None:
        prop_dict[props.PERIODS] = 1
        pa.add_props(prop_dict)
    else:
        result = utils.read_props(MODEL_NM)
        if result:
            pa.add_props(result.props)
        else:
            utils.ask_for_params(pa)
        
    
    # Now we create a minimal environment for our agents to act within:
    env = wm.WolframEnv("Wolfram Env",
                     pa["grid_width"],
                     pa["grid_height"],
                     model_nm=MODEL_NM,
                     props=pa,
                     rule_id=pa["rule_id"])
    
    # This env adds agents itself.
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
