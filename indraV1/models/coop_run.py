#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:13:15 2014
@author: Brandon and Gene
Implements Paul Krugman's babysitting co-op model.
"""

MODEL_NM = "coop"
import indra.prop_args2 as props   # noqa E402
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils   # noqa E402
import indra.prop_args as props   # noqa E402
import models.coop as cm   # noqa E402


def run(prop_dict=None):
    (prog_file, log_file,
     prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    global pa

    env = cm.CoopEnv(model_nm=MODEL_NM, props=pa)

    for i in range(pa["num_agents"]):
        env.add_agent(
            cm.CoopAgent('agent' + str(i), 5, 0))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
