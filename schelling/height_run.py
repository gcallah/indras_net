#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 16:45:50 2014

@author: Gene Callahan and Brandon Logan
"""
import indra.prop_args2 as props

MODEL_NM = "height"

START_HEIGHT = 100.0


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)
    import indra.utils as utils
    import schelling.height as hm
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    env = hm.HeightEnv(model_nm=MODEL_NM, props=pa)
    for i in range(pa["num_agents"]):
            env.add_agent(
                hm.HeightAgentEng('Eng agent' + str(i),
                                  START_HEIGHT, START_HEIGHT))
            env.add_agent(
                hm.HeightAgent('agent' + str(i), START_HEIGHT, START_HEIGHT))
    
    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
