#!/usr/bin/env python3
import logging
import prop_args as props
import entity as ent
import basic_model as bm

MODEL_NM = "basic_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

#logging.basicConfig(format='%(levelname)s:%(message)s',
#        level=logging.INFO, filemode='w', filename=LOG_FILE)


read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "basic.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 10)
    pa.set("user_type", ent.User.IPYTHON)


env = bm.BasicEnv(model_nm=MODEL_NM)
pa.set("env", env)

for i in range(pa.get("num_agents")):
    env.add_agent(
            bm.BasicAgent(name="agent" + str(i),
            goal="acting up!"))

logging.info("Starting program " + PROG_NM)
env.run()

