# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 16:45:50 2014

@author: Gene and Brandon
"""
import logging
import indra.utils as utils
import indra.prop_args as props
import height_model as hm

START_HEIGHT = 100.0

MODEL_NM = "height_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 80)

env = hm.HeightEnv(model_nm=MODEL_NM)

for i in range(pa.get("num_agents")):

        env.add_agent(
            hm.HeightAgentEng('Eng agent' + str(i),
                              START_HEIGHT, START_HEIGHT))
        env.add_agent(
            hm.HeightAgent('agent' + str(i), START_HEIGHT, START_HEIGHT))


logging.info("Starting program " + prog_file)

env.run()
