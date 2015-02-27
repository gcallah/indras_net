"""
A script to test our spatial capabilities.
"""

import logging
import indra.prop_args as props
import indra.user as user
import indra.grid_env as ge
import grid_model as gm

# set up some file names:
MODEL_NM = "grid_model"
PROG_NM = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "grid.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 11)
    pa.set("user_type", user.User.TERMINAL)
    pa.set("grid_width", 4)
    pa.set("grid_height", 4)

# Now we create a minimal environment for our agents to act within:
env = ge.GridEnv("Test grid env",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_agents")):
    env.add_agent(gm.TestGridAgent(name="agent" + str(i),
                  goal="taking up a grid space!"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + PROG_NM)

# let's test our iterator
for cell in env.occupied_iter(occupied=True):
    print("Contents of cell x = "
          + str(cell[1])
          + " and y = "
          + str(cell[2])
          + " is "
          + str(cell[0]))

# And now we set things running!
env.run()
