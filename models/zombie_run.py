#!/usr/bin/env python3
"""
A basic zombie model
"""
MODEL_NM = "zombie"

import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)
import indra.utils as utils
import models.zombie as zom

HUMAN_REPRO = 10
HUMAN_LIFEFORCE = 10

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    global pa 

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
        env.add_agent(zom.Human("Human" + str(i), "Reproducing", 
		## Delete the following comments when human attributes are fixed
                                pa["human_repro"]
                                pa["human_lforce"]
                                #HUMAN_REPRO,    #pa["human_repro"],
                                #HUMAN_LIFEFORCE,      #pa["human_lforce"],
                                rand_age=True))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
