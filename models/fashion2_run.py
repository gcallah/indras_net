"""
A fashion model with hipsters and followers.
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import fashion2_model as fm

# set up some file names:
MODEL_NM = "fashion2_model"
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
    pa.set("num_followers", 48)
    pa.set("num_hipsters", 16)
    pa.set("fmax_move", 2)
    pa.set("hmax_move", 2)
    pa.set("grid_width", 16)
    pa.set("grid_height", 16)

# Now we create a minimal environment for our agents to act within:
env = fm.Society("Society",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_followers")):
    env.add_agent(fm.Follower("follower" + str(i), "Looking like hipsters",
                              pa.get("fmax_move")))
for i in range(pa.get("num_hipsters")):
    env.add_agent(fm.Hipster("hipster" + str(i), "Looking trendy",
                             pa.get("hmax_move")))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
env.run()
env.record_results(results_file)
