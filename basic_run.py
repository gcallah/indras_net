#!/usr/bin/env python3
import logging
import prop_args as props
import entity as ent
import basic_model as bm

MODEL_NM = "basic_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

# print('globals:', globals())

read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "basic.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("num_agents", 10)
    pa.set("user_type", ent.User.TERMINAL)

logging.info("Starting program " + PROG_NM)

env = bm.BasicEnv(model_nm=MODEL_NM)

for i in range(pa.get("num_agents")):
    env.add_agent(
            bm.BasicAgent(name="agent" + str(i),
            goal="acting up!"))

env.run()

