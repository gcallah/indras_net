#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""

import indra.utils as utils
import indra.prop_args as props
import sand_model as sm

# set up some file names:
MODEL_NM = "grid_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.ask("grid_width", "What is the grid width?", int, default=200)
    pa.ask("grid_height", "What is the grid height?", int, default=200)

# Now we create a minimal environment for our agents to act within:
env = sm.SandEnv("Abelian sand env",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 model_nm=MODEL_NM)

# This env adds agents itself.

utils.run_model(env, prog_file, results_file)
