#!/usr/bin/env python3
"""
Runs a model with leaders and followers.
"""

import indra.utils as utils
import indra.prop_args as props
import stance_model as sm

# set up some file names:
MODEL_NM = "stance_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    utils.get_grid_dims(pa, 16)
    utils.get_agent_num(pa, "num_followers", "followers", 48)
    utils.get_agent_num(pa, "num_linvest", "leaders", 16)
    pa.ask("fmax_move", "What is the follower's max move?", int,
           default=4, limits=utils.GRID_LIMITS)
    pa.ask("lmax_move", "What is the leader's max move?", int,
           default=4, limits=utils.GRID_LIMITS)


# Now we create a minimal environment for our agents to act within:
env = sm.StanceEnv("Stance Environment",
                   pa.get("grid_height"),
                   pa.get("grid_width"),
                   torus=False,
                   model_nm=MODEL_NM)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_followers")):
    env.add_agent(sm.Follower("follower" + str(i), "Follow trend",
                              pa.get("fmax_move")))
for i in range(pa.get("num_linvest")):
    env.add_agent(sm.Leader("value" + str(i), "Lead trend",
                            pa.get("lmax_move")))

utils.run_model(env, prog_file, results_file)
