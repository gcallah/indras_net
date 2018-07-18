#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""
MODEL_NM = "Grid"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.grid_env as ge
import models.grid_model as gm
import logging


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
    
    if pa["user_type"] == props.WEB:
        pa["path"] = os.path.dirname(os.path.abspath(__file__))
    
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
