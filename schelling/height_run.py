#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 16:45:50 2014

@author: Gene Callahan and Brandon Logan
"""

import indra.utils as utils
import indra.prop_args as props
import schelling.height_model as hm

START_HEIGHT = 100.0

MODEL_NM = "height_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_agent_num(pa, "num_agents", "agents", 80)
    env = hm.HeightEnv(model_nm=MODEL_NM, props=pa)
    for i in range(pa.get("num_agents")):
            env.add_agent(
                hm.HeightAgentEng('Eng agent' + str(i),
                                  START_HEIGHT, START_HEIGHT))
            env.add_agent(
                hm.HeightAgent('agent' + str(i), START_HEIGHT, START_HEIGHT))
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
