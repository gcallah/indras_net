#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:13:15 2014
@author: Brandon and Gene
Implements Paul Krugman's babysitting co-op model.
"""

import indra.utils as utils
import indra.prop_args as props
import models.coop_model as cm

MODEL_NM = "coop_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        utils.get_agent_num(pa, "num_agents", "agents", 100)
        pa.ask("min_holdings",
               "What is a co-op member's minimum desired holding of coupons?",
               float, default=7.5, limits=(1.0, 20.0))
    
    env = cm.CoopEnv(model_nm=MODEL_NM, props=pa)
    
    for i in range(pa.get("num_agents")):
        env.add_agent(
            cm.CoopAgent('agent' + str(i), 5, 0))
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
