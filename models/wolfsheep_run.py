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
        utils.get_grid_dims(pa, 16)
        utils.get_agent_num(pa, "num_wolves", "wolves", 5)
        utils.get_agent_num(pa, "num_sheep", "sheep", 16)
        pa.ask("wolf_repro", "What is the wolf reproduction age?", int, default=16)
        pa.ask("wolf_lforce", "What is the wolf life force?", int, default=7)
        pa.ask("sheep_repro", "What is the sheep reproduction age?", int,
               default=3)
        pa.ask("sheep_lforce", "What is the sheep life force?", int, default=6)
    
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
