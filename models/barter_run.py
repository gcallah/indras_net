"""
A script to run our barter model.
"""

import logging
import indra.utils as utils
import indra.node as node
import indra.prop_args as props
import barter_model as bm

MODEL_NM = "barter_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
CSV_FILE = MODEL_NM + "02.csv"

read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file,
                        props=None)
    pa.set("model", MODEL_NM)
    pa.set("max_detect", 1000.0)

env = bm.BarterEnv("A barter market", 50.0, 50.0,
                   model_nm=MODEL_NM)
env.fetch_agents_from_file(CSV_FILE, bm.BarterAgent)

node.add_prehension(bm.BarterAgent, bm.TRADE, bm.BarterAgent)

logging.info("Starting program " + prog_file)
env.run()
env.record_results(results_file)
