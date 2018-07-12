#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:13:15 2014
@author: Brandon and Gene
Implements Paul Krugman's babysitting co-op model.
"""

MODEL_NM = "Coop"
import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.prop_args as props
import models.coop_model as cm


def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    global pa

    if prop_dict is not None:
        prop_dict[props.PERIODS] = 1
        pa.add_props(prop_dict)
    else:
        result = utils.read_props(MODEL_NM)
        if result:
            pa.add_props(result.props)
        else:
            utils.ask_for_params(pa)
    
    env = cm.CoopEnv(model_nm=MODEL_NM, props=pa)
    
    for i in range(pa["num_agents"]):
        env.add_agent(
            cm.CoopAgent('agent' + str(i), 5, 0))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
