#!/usr/bin/env python3
import logging
import prop_args as props
import entity as ent
import basic_model as bm

# set up some file names:
MODEL_NM = "basic_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "basic.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 10)
    pa.set("user_type", ent.User.IPYTHON_NB)

# Now we create a minimal environment for our agents to act within:
env = bm.BasicEnv(model_nm=MODEL_NM)
# And put the environment in the properties object:
pa.set("env", env)

# Now we loop creating multiple agents with numbered names based on the loop variable:
for i in range(pa.get("num_agents")):
    env.add_agent(
            bm.BasicAgent(name="agent" + str(i),
            goal="acting up!"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + PROG_NM)

# And now we set things running!
env.run()

print(ent.indras_net.edges())

