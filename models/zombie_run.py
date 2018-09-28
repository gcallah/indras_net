#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""
MODEL_NM = "grid"

import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.grid_env as ge
import models.grid as gm
import logging
import os


def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    global pa
    
    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ["base_dir"]
    
    # Now we create a minimal environment for our agents to act within:
    env = ge.GridEnv("Test grid env",
                     pa["grid_width"],
                     pa["grid_height"],
                     torus=False,
                     model_nm=MODEL_NM,
                     preact=True,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    for i in range(pa["num_agents"]):
        env.add_agent(gm.TestGridAgent(name="agent" + str(i),
                      goal="taking up a grid space!"))
    
    # let's test our iterator
    for cell in env:
        (x, y) = cell.coords
        logging.info("Contents of cell x = " + str(x)
              + " and y = " + str(y)
              + " is " + str(cell.contents))
        
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
