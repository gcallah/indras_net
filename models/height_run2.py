# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 16:45:50 2014

@author: Gene and Brandon
"""
import logging
import indra.prop_args as props
import height_model as hm

MODEL_NM = "height_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "height.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 10)
    #pa.set("parent_type", "GenEng")
    
env = hm.HeightEnv(model_nm=MODEL_NM)


for i in range(pa.get("num_agents")):
  
    if pa.get ("parent_type") == "GenEng":
        env.add_agent(
            hm.HeightAgentEng(name='Eng agent' + str(i),height = 8))
    else:
        env.add_agent(
            hm.HeightAgent(name='agent' + str(i),height = 8))


logging.info("Starting program " + PROG_NM)

env.run()