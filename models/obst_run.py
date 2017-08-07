#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""

import indra.utils as utils
import indra.prop_args as props
import indra.grid_env as ge
import models.obst_model as om

# set up some file names:
MODEL_NM = "obst_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_grid_dims(pa, 10)
        pa.set("num_moving_agents", 2)
        pa.set("num_obstacles", 4)
    
    # Now we create a minimal environment for our agents to act within:
    env = ge.GridEnv("Obstacle env",
                     pa.get("grid_height"),
                     pa.get("grid_width"),
                     torus=False,
                     model_nm=MODEL_NM,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    for i in range(pa.get("num_moving_agents")):
        env.add_agent(om.ObstacleAgent(name="agent" + str(i),
                      goal="Avoiding obstacles!", max_move=4,
                      tolerance=2))
    for i in range(pa.get("num_obstacles")):
        env.add_agent(om.Obstacle(name="obstacle" + str(i)))
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
