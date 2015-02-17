"""
A script to run our barter model.
"""

import logging
import indra.node as node
import indra.prop_args as props
import indra.barter_model as bm

MODEL_NM = "barter_model"
PROG_NM = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"
CSV_FILE = MODEL_NM + "02.csv"
PROPS_FILE = MODEL_NM + ".props"


read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, PROPS_FILE)
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE,
                        props=None)
    pa.set("model", MODEL_NM)
    pa.set("max_detect", 1000.0)

env = bm.BarterEnv("A barter market", 50.0, 50.0,
                   model_nm=MODEL_NM)
env.fetch_agents_from_file(CSV_FILE, bm.BarterAgent)

node.add_prehension(bm.BarterAgent, bm.TRADE, bm.BarterAgent)

logging.info("Starting program")
env.run()

