#!/usr/bin/env python3
"""
A predator-prey model with wolves and sheep.
"""
MODEL_NM = "Wolfsheep"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.prop_args as props
import models.wolfsheep_model as wsm

# set up some file names:

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
    
    # Now we create a meadow for our agents to act within:
    env = wsm.Meadow("Meadow",
                     pa["grid_width"],
                     pa["grid_height"],
                     model_nm=MODEL_NM,
                     preact=True,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the number of agents of that type to create:
    for i in range(pa["num_wolves"]):
        env.add_agent(wsm.Wolf("wolf" + str(i), "Eating sheep",
                               pa["wolf_repro"],
                               pa["wolf_lforce"],
                               rand_age=True))
    for i in range(pa["num_sheep"]):
        env.add_agent(wsm.Sheep("sheep" + str(i), "Reproducing",
                                pa["sheep_repro"],
                                pa["sheep_lforce"],
                                rand_age=True))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
