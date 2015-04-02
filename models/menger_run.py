#!/usr/bin/env python3
"""
A script to run our Menger model.
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import indra.node as node
import barter_model as bm
import menger_model as mm

# set up some file names:
MODEL_NM = "menger_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
CSV_FILE = MODEL_NM + "02.csv"

# We store basic parameters in a
# "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file,
                        loglevel=logging.INFO, props=None)
    pa.set("model", MODEL_NM)
    pa.set("prod_amt", 1)

# Now we create an environment for our agents to act within:
env = mm.MengerEnv("Menger's money model", 50.0, 50.0,
                   model_nm=MODEL_NM)
env.fetch_agents_from_file(CSV_FILE, mm.MengerAgent)
env.add_prod_goods()

node.add_prehension(mm.MengerAgent, bm.TRADE, mm.MengerAgent)

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
env.run()
env.record_results(results_file)
