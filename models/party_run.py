#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:39:40 2015

@author: Brandon Logan and Gene Callahan

Party Run File
"""

import indra.prop_args2 as props
import os

MODEL_NM = "party"


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.party as pm

    # set up some file names:
    (prog_file, log_file, prop_file,
     results_file) = utils.gen_file_names(MODEL_NM)
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.

    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ['base_dir']

    # Now we create an environment for our agents to act within:
    env = pm.PartyEnv("A cocktail party",
<<<<<<< HEAD
                            pa["grid_width"],
                            pa["grid_height"],
                            model_nm=pa.model_nm,
                            props=pa)
    
=======
                      pa["grid_width"],
                      pa["grid_height"],
                      model_nm=pa.model_nm,
                      props=pa)

>>>>>>> 71cbb6374957a716fc9a0c5661862edf2e6c609b
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    for i in range(pa["num_men"]):
        env.add_agent(pm.Man(name="Man" + str(i),
                      goal="A good party.",
                      tol=0.5,
                      max_detect=pa['max_detect']))

    for i in range(pa["num_women"]):
        env.add_agent(pm.Woman(name="Woman" + str(i),
                      goal="A good party.",
                      tol=0.5,
                      max_detect=pa['max_detect']))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
