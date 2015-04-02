#!/usr/bin/env python3
"""
This file runs the forestfire_model.
"""

import logging
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
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)

GRID_X = 100
GRID_Y = 100
DENSITY = .416

# Now we create a forest environment for our agents to act within:
env = fm.ForestEnv(GRID_X, GRID_Y, DENSITY, model_nm=MODEL_NM, torus=False)
num_agents = int(GRID_X * GRID_Y * DENSITY)

for i in range(num_agents):
    env.add_agent(fm.Tree(name="tree" + str(i)))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
env.run()
env.record_results(results_file)
