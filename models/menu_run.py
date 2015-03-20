#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""

import logging
import indra.prop_args as props
import menu_model as mm

# set up some file names:
MODEL_NM = "menu_model"
PROG_NM = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

# We store menu parameters in a
# "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "menu.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 10)

# Now we create a minimal environment for our agents to act within:
env = mm.MenuEnv(model_nm=MODEL_NM)

# Now we loop creating multiple agents
#  with numbered names based on the loop variable:
for i in range(pa.get("num_agents")):
    env.add_agent(mm.MenuAgent(name="agent" + str(i),
                               goal="testing our menu capabilities!"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + PROG_NM)

# And now we set things running!
env.run()
