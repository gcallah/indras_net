#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:39:40 2015

@author: Brandon

Segregation Run File
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import segregation_model as sm

# set up some file names:
MODEL_NM = "segregation_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_R_agents", 1100)
    pa.set("num_B_agents", 1100)
    pa.set("grid_width", 60)
    pa.set("grid_height", 60)
    pa.ask("tolerance", "What is the agent's minimum % like self tolerated?",
           float)
    pa.ask("hoodsize", "What is the agent's neighborhood size?", int)

# Now we create an environment for our agents to act within:
env = sm.SegregationEnv("A city",
                        pa.get("grid_height"),
                        pa.get("grid_width"))

# Now we loop creating multiple agents with numbered names
# based on the loop variable:

for i in range(pa.get("num_B_agents")):
    env.add_agent(sm.BlueAgent(name="Blue agent" + str(i),
                  goal="A preferred neighborhood.",
                  tolerance=pa.get('tolerance'),
                  nsize=pa.get('hoodsize')))

for i in range(pa.get("num_R_agents")):
    env.add_agent(sm.RedAgent(name="Red agent" + str(i),
                  goal="A good neighborhood.",
                  tolerance=pa.get('tolerance'),
                  nsize=pa.get('hoodsize')))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
env.run()
env.record_results(results_file)
