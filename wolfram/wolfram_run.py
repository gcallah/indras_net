#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""

import indra.utils as utils
import indra.prop_args as props
import Wolfram.wolfram_model as wm
# set up some file names:
MODEL_NM = "wolfram_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_grid_dims(pa, 50)
        utils.get_rule_id(pa, 30)
        
    
    # Now we create a minimal environment for our agents to act within:
    env = wm.WolframEnv("Wolfram Env",
                     pa.get("grid_width"),
                     pa.get("grid_height"),
                     model_nm=MODEL_NM,
                     props=pa,
                     rule_id=pa.get("rule_id"))
    
    # This env adds agents itself.
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
