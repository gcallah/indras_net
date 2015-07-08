#!/usr/bin/env python3
"""
emp_run.py
A script to run our simple employee model,
demonstrating heirarchical graphing.
"""

import indra.utils as utils
import indra.prop_args as props
import emp_model as em

# set up some file names:
MODEL_NM = "emp_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a
# "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)

# Now we create a minimal environment for our agents to act within:
env = em.EmpEnv(model_nm=MODEL_NM)

linda = em.EmpAgent("Linda")
suzanne = em.EmpAgent("Suzanne")
sandy = em.EmpAgent("Sandy")
connie = em.EmpAgent("Connie")
rich = em.EmpAgent("Rich")
gene = em.EmpAgent("Gene")
shruti = em.EmpAgent("Shruti")
cedric = em.EmpAgent("Cedric")

em.employs(sandy, gene)
em.employs(sandy, shruti)
em.employs(sandy, cedric)
em.employs(linda, connie)
em.employs(linda, sandy)
em.employs(suzanne, linda)
em.employs(suzanne, rich)

utils.run_model(env, prog_file, results_file)
