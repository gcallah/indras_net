#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""

import time
import logging
import indra.utils as utils
import indra.prop_args as props
import timer_model as tm

# set up some file names:
MODEL_NM = "timer_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a
# "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("num_agents", 50)

# Now we create a minimal environment for our agents to act within:
env = tm.TimerEnv(model_nm=MODEL_NM)

# Now we loop creating multiple agents
#  with numbered names based on the loop variable:
for i in range(pa.get("num_agents")):
    env.add_agent(tm.TimerAgent1(name="agent" + str(i),
                                 goal="acting up!"))
    env.add_agent(tm.TimerAgent2(name="agent" + str(i),
                                 goal="acting up!"))
    env.add_agent(tm.TimerAgent3(name="agent" + str(i),
                                 goal="acting up!"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
print(time.clock())
env.run(loops=10000)
print(time.clock())
