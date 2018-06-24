#!/usr/bin/env python3
"""
A script to test our two pop capabilities.
"""

import indra.utils as utils
import indra.prop_args as props
import indra.two_pop_model as itpm
import models.two_pop_model as tpm

# set up some file names:
MODEL_NM = "two_pop_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_grid_dims(pa, 6)
        utils.get_agent_num(pa, "num_agents", "agents", 8)
    
    # Now we create a minimal environment for our agents to act within:
    env = itpm.TwoPopEnv("Test grid env",
                     pa.get("grid_width"),
                     pa.get("grid_height"),
                     torus=False,
                     model_nm=MODEL_NM,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    
    # Get Number of Followers
    for i in range(pa.get("num_agents")):
        env.add_agent(tpm.TestFollower(name="Follower" + str(i),
                      goal="taking up a grid space!",max_move=1))
    
    # Get Number of Hipsters
    for i in range(pa.get("num_agents")):
        env.add_agent(tpm.TestLeader(name="Leader" + str(i),
                      goal="taking up a grid space!",max_move=1))
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
