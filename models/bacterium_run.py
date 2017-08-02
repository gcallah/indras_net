#!/usr/bin/env python3
"""
A script to run the bacterium model.
"""

import indra.utils as utils
import indra.prop_args as props
import indra.grid_env as ge
import models.bacterium_model as bm

# set up some file names:
MODEL_NM = "grid_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("num_agents", 1)
    pa.set("grid_width", 4)
    pa.set("grid_height", 4)

# Now we create a minimal environment for our agents to act within:
env = ge.GridEnv("Test grid env",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM,
                 postact=True)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
"""
for i in range(pa.get("num_agents")):
"""

# Add our bacterium and our food source to the env
env.add_agent(bm.Bacterium(name="Rick", goal="work"))

env.add_agent(bm.FoodSource(name="Runaway Food", goal="not get eaten"))

utils.run_model(env, prog_file, results_file)
