#!/usr/bin/env python3
"""
A predator-prey model with wolves and sheep.
"""

import indra.utils as utils
import indra.prop_args as props
import models.wolfsheep_model as wsm

# set up some file names:
MODEL_NM = "wolfsheep_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    
    # Now we create a meadow for our agents to act within:
    env = wsm.Meadow("Meadow",
                     pa.get("grid_width"),
                     pa.get("grid_height"),
                     model_nm=MODEL_NM,
                     preact=True,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the number of agents of that type to create:
    for i in range(pa.get("num_wolves")):
        env.add_agent(wsm.Wolf("wolf" + str(i), "Eating sheep",
                               pa.get("wolf_repro"),
                               pa.get("wolf_lforce"),
                               rand_age=True))
    for i in range(pa.get("num_sheep")):
        env.add_agent(wsm.Sheep("sheep" + str(i), "Reproducing",
                                pa.get("sheep_repro"),
                                pa.get("sheep_lforce"),
                                rand_age=True))
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
