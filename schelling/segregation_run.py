#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:39:40 2015

@author: Brandon Logan and Gene Callahan

Segregation Run File
"""

import indra.utils as utils
import indra.prop_args as props
import schelling.segregation_model as sm

# set up some file names:
MODEL_NM = "segregation_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_grid_dims(pa, 60)
        utils.get_agent_num(pa, "num_R_agents", "red agents", 1100)
        utils.get_agent_num(pa, "num_B_agents", "blue agents", 1100)
        utils.get_pct(pa, "max_tolerance", "agent", "minimum intolerance", .10)
        utils.get_pct(pa, "min_tolerance", "agent", "maximum intolerance", .70)
        pa.ask("max_detect", "What is the agent's neighborhood size?",
               int, default=4, limits=(1, 10))
    # Now we create an environment for our agents to act within:
    env = sm.SegregationEnv("A city",
                            pa.get("grid_width"),
                            pa.get("grid_height"),
                            props=pa)
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    for i in range(pa.get("num_B_agents")):
        env.add_agent(sm.BlueAgent(name="Blue agent" + str(i),
                      goal="A good neighborhood.",
                      min_tol=pa.get('min_tolerance'),
                      max_tol=pa.get('max_tolerance'),
                      max_detect=pa.get('max_detect')))
    for i in range(pa.get("num_R_agents")):
        env.add_agent(sm.RedAgent(name="Red agent" + str(i),
                      goal="A good neighborhood.",
                      min_tol=pa.get('min_tolerance'),
                      max_tol=pa.get('max_tolerance'),
                      max_detect=pa.get('max_detect')))
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
