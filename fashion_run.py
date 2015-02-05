#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
"""
fashion_run.py: A script to run fashion+model.py,
which implements Adam Smith's fashion model.
"""

import logging
import node
import prop_args as props
import predprey_model as ppm
import fashion_model as fm

MODEL_NM = "fashion_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "fashion.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)

    pa.set("model", MODEL_NM)
    
    pa.set("num_trndstr", 20)
    pa.set("num_flwr", 80)
    
    pa.set("fshn_f_ratio", 1.3)
    pa.set("fshn_t_ratio", 1.5)
    
    pa.set("flwr_others", 3)
    pa.set("trnd_others", 5)
    
    pa.set("flwr_max_detect", 20.0)
    pa.set("trnd_max_detect", 20.0)

    pa.set("min_adv_periods", 8)

env = fm.SocietyEnv("society", 50.0, 50.0, model_nm=MODEL_NM)

for i in range(pa.get("num_flwr")):
    env.add_agent(fm.Follower(name="prole" + str(i),
                  max_detect=pa.get("flwr_max_detect")))

for i in range(pa.get("num_trndstr")):
    env.add_agent(fm.TrendSetter(name="hipster" + str(i),
                  max_detect=pa.get("trnd_max_detect")))

node.add_prehension(fm.Follower, ppm.EAT, fm.TrendSetter)
node.add_prehension(fm.TrendSetter, ppm.AVOID, fm.Follower)

logging.info("Starting program")
env.run()
