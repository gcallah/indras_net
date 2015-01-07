import sys
import logging
import prop_args as props
import entity as ent
import barter_market_model as bmm

MODEL_NM = "barter_market_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"


read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "barter_market_model.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
#    pa.set("user_type", ent.User.IPYTHON_NB)
    pa.set("model", MODEL_NM)
    pa.set("al_cheese", 20)
    pa.set("al_cutil", "10 - .5 * qty")
    pa.set("al_wine", 0)
    pa.set("al_wutil", "10 - .75 * qty")
    pa.set("al_olive", 0)
    pa.set("al_outil", "10 - .25 * qty")
    pa.set("bea_wine", 20)
    pa.set("bea_wutil", "10 - .5 * qty")
    pa.set("bea_cheese", 0)
    pa.set("bea_cutil", "10 - .75 * qty")
    pa.set("bea_olive", 0)
    pa.set("bea_outil", "10 - .25 * qty")
    pa.set("cha_wine", 0)
    pa.set("cha_wutil", "10 - .5 * qty")
    pa.set("cha_cheese", 0)
    pa.set("cha_cutil", "10 - .25 * qty")
    pa.set("cha_olive", 20)
    pa.set("cha_outil", "10 - .25 * qty")


logging.info("Starting program")


env = bmm.BartermarketEnv("A barter market", 50.0, 50.0, model_nm=MODEL_NM)
pa.set("env", env)

albert = bmm.BarterMarketAgent(name="Albert")
env.add_agent(albert)
albert.endow(bmm.CHEESE,
                pa.get("al_cheese"),
                util_func=eval("lambda qty: " + pa.get("al_cutil")))
albert.endow(bmm.WINE,
                pa.get("al_wine"),
                util_func=eval("lambda qty: " + pa.get("al_wutil")))
albert.endow(bmm.OLIVE_OIL,
                pa.get("al_olive"),
                util_func=eval("lambda qty: " + pa.get("al_outil")))

beatrice = bmm.BarterMarketAgent(name="Beatrice")
env.add_agent(beatrice)
beatrice.endow(bmm.WINE,
                pa.get("bea_wine"),
                util_func=eval("lambda qty: " + pa.get("bea_wutil")))
beatrice.endow(bmm.CHEESE,
                pa.get("bea_cheese"),
                util_func=eval("lambda qty: " + pa.get("bea_cutil")))
beatrice.endow(bmm.OLIVE_OIL,
                pa.get("bea_olive"),
                util_func=eval("lambda qty: " + pa.get("bea_outil")))

charles = bmm.BarterMarketAgent(name="Charles")
env.add_agent(charles)
charles.endow(bmm.WINE,
                pa.get("cha_wine"),
                util_func=eval("lambda qty: " + pa.get("cha_wutil")))
charles.endow(bmm.CHEESE,
                pa.get("cha_cheese"),
                util_func=eval("lambda qty: " + pa.get("cha_cutil")))
charles.endow(bmm.OLIVE_OIL,
                pa.get("cha_olive"),
                util_func=eval("lambda qty: " + pa.get("cha_outil")))

ent.Entity.add_universal(bmm.BarterMarketAgent, bmm.TRADE, bmm.BarterMarketAgent)

env.run()

