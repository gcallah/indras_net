#!/usr/bin/env python3
"""
A script that runs big_box_model. It simulates the market economy
of consumers, mom and pops, and big boxes.
"""

import indra.utils as utils
import indra.prop_args as props
import big_box_model as bb

# set up some file names:
MODEL_NM = "big_box_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    utils.get_grid_dims(pa, 50)
    utils.get_agent_num(pa, "num_consumers", "consumers", bb.NUM_GOODS * 5)
    utils.get_agent_num(pa, "num_mom_and_pops", "mom and pop stores",
                        bb.NUM_GOODS)
    pa.ask("allowance", "What are the consumers' daily allowances?", 
           int, default=2)
    pa.ask("endowment", "What are the small shops' initial endowments?", 
           int, default=20)
    # We should ask this for big boxes as well!
    pa.ask("rent", "What are the stores' rents?", int, default=7)
    # We should ask this for big boxes as well!

# Now we create a meadow for our agents to act within:
env = bb.EverytownUSA(pa.get("grid_width"),
                      pa.get("grid_height"),
                      model_nm=MODEL_NM)

# Now we loop creating multiple agents with numbered names
# based on the number of agents of that type to create:
for i in range(pa.get("num_consumers")):
    env.add_agent(bb.Consumer("consumer" + str(i),
                              goal=(i % bb.NUM_GOODS),
                              init_state=0,
                              allowance=pa.get("allowance")))
for i in range(pa.get("num_mom_and_pops")):
    env.add_agent(bb.MomAndPop("mom_and_pop" + str(i),
                                 goal=(i % bb.NUM_GOODS),
                                 endowment=pa.get("endowment"),
                                 rent=pa.get("rent")))

env.add_agent(bb.BigBox("Big Box", goal="Dominance",
                        endowment=(pa.get("endowment") * 1000),
                        rent=(pa.get("rent") * 2)))

utils.run_model(env, prog_file, results_file)
