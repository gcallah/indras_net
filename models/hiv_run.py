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

MODEL_NM = "hiv"
INI_INFECTED_PCT = .025
STD_COUP_TEND = 1
STD_TEST_FREQ = 0.2
STD_COMMITMENT = 20
STD_CONDOM_USE = 1


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)
    (prog_file, log_file, prop_file,
     results_file) = utils.gen_file_names(MODEL_NM)

    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ["base_dir"]

    grid_x = pa["grid_width"]
    grid_y = pa["grid_height"]
    ini_ppl = pa["ini_ppl"]
    avg_coup_tend = pa["avg_coup_tend"]
    avg_test_freq = pa["avg_test_freq"]
    avg_commitment = pa["avg_commitment"]
    avg_condom_use = pa["avg_condom_use"]

    max_ppl = grid_x * grid_y

    if ini_ppl > max_ppl:
        ini_ppl = max_ppl

    # Now we create an environment for our agents to act within:
    env = hiv.People("People", grid_x, grid_y, model_nm=MODEL_NM,
                     preact=True, postact=True, props=pa)

    ini_infected_ppl = round(INI_INFECTED_PCT * ini_ppl)
    ini_healthy_ppl = ini_ppl - ini_infected_ppl
    # print("initial infected people:", ini_infected_ppl)
    # print("initial healthy people:", ini_healthy_ppl)

    coup_tend = numpy.random.normal(avg_coup_tend, STD_COUP_TEND, ini_ppl)
    test_freq = numpy.random.normal(avg_test_freq, STD_TEST_FREQ, ini_ppl)
    commitment = numpy.random.normal(avg_commitment, STD_COMMITMENT, ini_ppl)
    condom_use = numpy.random.normal(avg_condom_use, STD_CONDOM_USE, ini_ppl)
    for i in range(ini_ppl):
        if coup_tend[i] < 0:
            coup_tend[i] = 0
        elif coup_tend[i] > 10:
            coup_tend[i] = 10
        if test_freq[i] < 0:
            test_freq[i] = 0
        elif test_freq[i] > 2:
            test_freq[i] = 2
        if commitment[i] < 1:
            commitment[i] = 1
        elif commitment[i] > 200:
            commitment[i] = 200
        if condom_use[i] < 0:
            condom_use[i] = 0
        elif condom_use[i] > 10:
            condom_use[i] = 10

    for i in range(ini_infected_ppl):
        rand_inf_len = random.randint(0, hiv.SYMPTOMS_SHOW-1)
        new_agent = hiv.Person(name="person" + str(i),
                               infected=True,
                               infection_length=rand_inf_len,
                               initiative=i,
                               coupling_tendency=coup_tend[i],
                               test_frequency=test_freq[i],
                               commitment=commitment[i],
                               condom_use=condom_use[i])
        env.add_agent(new_agent)
    for i in range(ini_healthy_ppl):
        new_agent = hiv.Person(name="person" + str(ini_infected_ppl+i),
                               infected=False, infection_length=0,
                               initiative=ini_infected_ppl+i,
                               coupling_tendency=coup_tend[ini_infected_ppl+i],
                               test_frequency=test_freq[ini_infected_ppl+i],
                               commitment=commitment[ini_infected_ppl+i],
                               condom_use=condom_use[ini_infected_ppl+i])
        env.add_agent(new_agent)

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
