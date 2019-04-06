#!/usr/bin/env python3
"""
A predator-prey model with wolves and sheep.
"""

import indra.prop_args2 as props

MODEL_NM = "wolfsheep"


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.wolfsheep as wsm
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    # we create a meadow for our agents to act within:
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
