import sys
import logging
import prop_args as props
import entity as ent
import barter_model as bm

MODEL_NM = "barter_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"
CSV_FILE = MODEL_NM + ".csv"
PROPS_FILE = MODEL_NM + ".props"


read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, PROPS_FILE)
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE,
                        props=None)
    pa.set("model", MODEL_NM)

env = bm.BarterEnv("A barter market", 50.0, 50.0,
                    model_nm=MODEL_NM)
pa.set("env", env)
env.fetch_agents_from_file(CSV_FILE)


#charles = bm.BarterAgent(name="Charles")
#env.add_agent(charles)
#charles.endow(bm.WINE,
#                pa.get("cha_wine"),
#                util_func=eval("lambda qty: " + pa.get("cha_wutil")))
#charles.endow(bm.CHEESE,
#                pa.get("cha_cheese"),
#                util_func=eval("lambda qty: " + pa.get("cha_cutil")))
#charles.endow(bm.OLIVE_OIL,
#                pa.get("cha_olive"),
#                util_func=eval("lambda qty: " + pa.get("cha_outil")))

ent.Entity.add_universal(bm.BarterAgent, bm.TRADE, bm.BarterAgent)

logging.info("Starting program")
env.run()

