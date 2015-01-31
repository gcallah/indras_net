#!/usr/bin/env python3
"""
A script to run our Menger model.
"""

import logging
import prop_args as props
import node
import entity as ent
import barter_model as bm
import menger_model as mm

# set up some file names:
MODEL_NM = "menger_model"
PROG_NM = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"
CSV_FILE = MODEL_NM + ".csv"
PROPS_FILE = MODEL_NM + ".props"

# We store basic parameters in a
# "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, PROPS_FILE)
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE,
                        loglevel=logging.DEBUG, props=None)
    pa.set("model", MODEL_NM)
    pa.set("user_type", ent.User.TERMINAL)

# Now we create an environment for our agents to act within:
env = mm.MengerEnv("Menger's money model", 50.0, 50.0,
                   model_nm=MODEL_NM)
env.fetch_agents_from_file(CSV_FILE, mm.MengerAgent)
env.add_prod_goods()

node.add_prehension(mm.MengerAgent, bm.TRADE, mm.MengerAgent)

# Logging is automatically set up for the modeler:
logging.info("Starting program " + PROG_NM)

# And now we set things running!
env.run()

