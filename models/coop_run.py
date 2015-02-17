# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:13:15 2014

@author: Brandon
"""


import logging
import prop_args as props
import entity as ent
import coop_model as cm

MODEL_NM = "coop_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "coop.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 10)
    pa.set("user_type", ent.User.IPYTHON_NB)
    
env = cm.CoopEnv(model_nm=MODEL_NM)


for i in range(pa.get("num_agents")):
    env.add_agent(
        cm.CoopAgent('agent' + str(i), i+1))


logging.info("Starting program " + PROG_NM)

env.run()