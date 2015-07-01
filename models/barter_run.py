#!/usr/bin/env python3
"""
A script to run our barter model.
"""

import indra.utils as utils
import indra.node as node
import indra.prop_args as props
import edgebox_model as ebm
import barter_model as bm

MODEL_NM = "barter_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
CSV_FILE = MODEL_NM + "02.csv"

read_props = False

pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file,
                        props=None)
    pa.set("model", MODEL_NM)
    pa.ask("max_detect", "What is the trader detect distance?", int,
           default=ebm.GLOBAL_KNOWLEDGE)
    pa.ask("grid_dim", "What is the length of the grid's sides?",
           int, default=50)

dim = pa.get("grid_dim")
env = bm.BarterEnv("A barter market", dim, dim, model_nm=MODEL_NM)
env.fetch_agents_from_file(CSV_FILE, bm.BarterAgent)

node.add_prehension(bm.BarterAgent, bm.TRADE, bm.BarterAgent)

utils.run_model(env, prog_file, results_file)
