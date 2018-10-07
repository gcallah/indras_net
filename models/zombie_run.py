#!/usr/bin/env python3

MODEL_NM = "zombie"

import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)
import indra.utils as utils
import indra.prop_args as props
import models.zombie as zom

# set up some file names:

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    global pa ##  <--- My guy, do you have a license for this??

    # we create a meadow for our agents to act within:
    env = zom.Zone("Infected Zone",
                     pa["grid_width"],
                     pa["grid_height"],
                     model_nm=MODEL_NM,
                     preact=True,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the number of agents of that type to create:
    for i in range(pa["num_zombies"]):
        env.add_agent(zom.Zombie("Zombie" + str(i), "Eating Human",
                               pa["zombie_repro"],
                               pa["zombie_lforce"],
                               rand_age=True))
    for i in range(pa["num_humans"]):
	#### We need to add human attributes to make this part work.
	#### We need to add module functions in a more working manner
        env.add_agent(zom.Human("Human" + str(i), "Reproducing", 
		## Delete the following comments when human attributes are fixed
                                4,#pa["human_repro"],
                                4,#pa["human_lforce"],
                                rand_age=True))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
