#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""
MODEL_NM = "wolfram"


import indra.prop_args2 as props
import os

def run(prop_dict=None):
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import wolfram.wolfram as wm
    import indra.utils as utils
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    
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
