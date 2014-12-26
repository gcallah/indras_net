import sys
import logging
import prop_args as pa
import entity
import edgebox_model as ebm

MODEL_NM = "edgebox_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"


read_props = False

if read_props:
    props = pa.PropArgs.read_props(MODEL_NM, "edgebox_props.txt")
else:
    props = pa.PropArgs(MODEL_NM, LOG_FILE)

logging.info("Starting program")


env = EdgeboxEnv(50.0, 50.0, model_nm=MODEL_NM)

env.add_agent(EdgeboxAgent(name="Albert"))
env.add_agent(EdgeboxAgent(name="Beatrice"))

entity.Entity.add_universal(EdgeboxAgent, ebm.TRADE, EdgeboxAgent)

env.run()

