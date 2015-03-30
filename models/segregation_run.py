# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:39:40 2015

@author: Brandon

Segregation Run File
"""

import logging
import indra.prop_args as props
import indra.user as user
import indra.grid_env as ge
import segregation_model as sm

# set up some file names:
MODEL_NM = "segregation_model"
PROG_NM = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "segregation.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_R_agents", 50)
    pa.set("num_B_agents", 20)
    pa.set("num_G_agents", 20)
    pa.set("grid_width", 10)
    pa.set("grid_height", 10)
    pa.set("tolerance", .5)

# Now we create a minimal environment for our agents to act within:
env = ge.GridEnv("Test grid env",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM,
                 postact=True)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_R_agents")):
    env.add_agent(sm.RedAgent(name="Red agent" + str(i),
                  goal="taking up a grid space!", tolerance = pa.get('tolerance')))

for i in range(pa.get("num_B_agents")):
    env.add_agent(sm.BlueAgent(name="Blue agent" + str(i),
                  goal="taking up a grid space!", tolerance = pa.get('tolerance')))
                  
for i in range(pa.get("num_G_agents")):
    env.add_agent(sm.GreenAgent(name="Green agent" + str(i),
                  goal="taking up a grid space!", tolerance = pa.get('tolerance')))                  

# Logging is automatically set up for the modeler:
logging.info("Starting program " + PROG_NM)

# let's test our iterator
#for cell in env.occupied_iter(occupied=True):
#    print("Contents of cell x = "
#          + str(cell[1])
#          + " and y = "
#          + str(cell[2])
#          + " is "
#          + str(cell[0]))

# And now we set things running!
env.run()
