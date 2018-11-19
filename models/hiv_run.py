#!/usr/bin/env python3
"""
    This file runs the hiv model
    """
import indra.prop_args2 as props
import os
import random
import numpy
import indra.utils as utils
import models.hiv as hiv

MODEL_NM = "HIV"
INI_INFECTED_PCT = .025

def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ["base_dir"]

    '''
    grid_x = pa["grid_width"]
    grid_y = pa["grid_height"]
    ini_ppl = pa["ini_ppl"]
    avg_coup_tend = pa["avg_coup_tend"]
    avg_test_freq = pa["avg_test_freq"]
    avg_commitment = pa["avg_commitment"]
    avg_condom_use = pa["avg_condom_use"]
    '''

    grid_x = 5
    grid_y = 5
    ini_ppl = 10
    avg_coup_tend = 5
    avg_test_freq = 0
    avg_commitment = 50
    avg_condom_use = 0

    print(grid_x, grid_y, ini_ppl, avg_coup_tend, avg_test_freq, avg_commitment, avg_condom_use)

    # Now we create an environment for our agents to act within:
    env = hiv.People("People", grid_x, grid_y, model_nm=MODEL_NM, preact=True, postact=True, props=pa)

    ini_infected_ppl = round(INI_INFECTED_PCT * ini_ppl)
    ini_healthy_ppl = ini_ppl - ini_infected_ppl

    coup_tend = numpy.random.normal(avg_coup_tend, 1, ini_ppl)
    test_freq = numpy.random.normal(avg_test_freq, 1, ini_ppl)
    commitment = numpy.random.normal(avg_commitment, 1, ini_ppl)
    condom_use = numpy.random.normal(avg_condom_use, 1, ini_ppl)

    for i in range(ini_infected_ppl):
        env.add_agent(hiv.Person(name="person" + str(i), infected=True, infection_length=random.randint(0, hiv.SYMPTOMS_SHOW-1), coupling_tendency=coup_tend[i], test_frequency=test_freq[i], commitment=commitment[i], condom_use=condom_use[i]))
    for i in range(ini_healthy_ppl):
        env.add_agent(hiv.Person(name="person" + str(ini_infected_ppl+i), infected=False, infection_length=0, coupling_tendency=coup_tend[ini_infected_ppl+i], test_frequency=test_freq[ini_infected_ppl+i], commitment=commitment[ini_infected_ppl+i], condom_use=condom_use[ini_infected_ppl+i]))

    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
