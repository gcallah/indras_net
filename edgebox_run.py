"""
edgebox_run.py
The script to run our Edgeworth Box model.
"""

import logging
import prop_args as props
import node
import edgebox_model as ebm

MODEL_NM = "edgebox_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "edgebox.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
#    pa.set("user_type", ent.User.IPYTHON_NB)
    pa.set("model", MODEL_NM)
    pa.set("al_cheese", 20)
    pa.set("al_cutil", "10 - .5 * qty")
    pa.set("al_wine", 0)
    pa.set("al_wutil", "10 - .75 * qty")
    pa.set("bea_wine", 20)
    pa.set("bea_wutil", "10 - .5 * qty")
    pa.set("bea_cheese", 0)
    pa.set("bea_cutil", "10 - .75 * qty")

env = ebm.EdgeboxEnv("An Edgeworth Box", 50.0, 50.0, model_nm=MODEL_NM)

albert = ebm.EdgeboxAgent(name="Albert")
env.add_agent(albert)
albert.endow(ebm.CHEESE,
             pa.get("al_cheese"),
             util_func=eval("lambda qty: " + pa.get("al_cutil")))
albert.endow(ebm.WINE,
             pa.get("al_wine"),
             util_func=eval("lambda qty: " + pa.get("al_wutil")))

beatrice = ebm.EdgeboxAgent(name="Beatrice")
env.add_agent(beatrice)
beatrice.endow(ebm.WINE,
               pa.get("bea_wine"),
               util_func=eval("lambda qty: " + pa.get("bea_wutil")))
beatrice.endow(ebm.CHEESE,
               pa.get("bea_cheese"),
               util_func=eval("lambda qty: " + pa.get("bea_cutil")))

node.add_prehension(ebm.EdgeboxAgent, ebm.TRADE, ebm.EdgeboxAgent)

logging.info("Starting program")
env.run()

