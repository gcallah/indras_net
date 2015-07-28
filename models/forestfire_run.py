#!/usr/bin/env python3
"""
This file runs the forestfire_model.
"""

import indra.prop_args as props
import indra.utils as utils
import forestfire_model as fm

# set up some file names:
MODEL_NM = "forestfire_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a
# "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    utils.get_grid_dims(pa, 100)
    pa.ask("density", "How dense is the forest?", float,
           default=.43, limits=utils.BTWN_ZERO_ONE)
    pa.ask("strike_freq", "How many turns between lightning strikes?",
           int, default=4, limits=utils.POS_INTS)
    pa.ask("regen_period",
           "How many turns before a new tree grows where one has burned?",
           int, default=20, limits=utils.POS_INTS)

density = pa.get("density")
grid_x = pa.get("grid_width")
grid_y = pa.get("grid_height")

# Now we create a forest environment for our agents to act within:
env = fm.ForestEnv(grid_x, grid_y, density, pa.get("strike_freq"),
                   pa.get("regen_period"), model_nm=MODEL_NM, torus=False)
num_agents = int(grid_x * grid_y * density)

for i in range(num_agents):
    env.add_agent(fm.Tree(name="tree" + str(i)))

utils.run_model(env, prog_file, results_file)
