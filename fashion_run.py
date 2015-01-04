import logging
import entity as ent
import prop_args as props
import predprey_model as ppm
import fashion_model as fm

MODEL_NM = "fashion_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + "_log.txt"


read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "fashion.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    
    pa.set("num_trndstr", 20)
    pa.set("num_flwr", 80)
    
    pa.set("fshn_f_ratio", 1.3)
    pa.set("fshn_t_ratio", 1.5)
    
    pa.set("flwr_others", 3)
    pa.set("trnd_others", 5)
    
    pa.set("flwr_max_detect", 20.0)
    pa.set("trnd_max_detect", 20.0)

    pa.set("min_adv_periods", 8)


logging.info("Starting program")

env = fm.SocietyEnv("society", 50.0, 50.0, model_nm=MODEL_NM)

for i in range(pa.get("num_flwr")):
    env.add_agent(
            fm.Follower(name="prole" + str(i),
                max_detect=pa.get("flwr_max_detect")))

for i in range(pa.get("num_trndstr")):
    env.add_agent(
            fm.TrendSetter(name="hipster" + str(i),
                max_detect=pa.get("trnd_max_detect")))

ent.Entity.add_universal(fm.Follower, ppm.EAT, fm.TrendSetter)
ent.Entity.add_universal(fm.TrendSetter, ppm.AVOID, fm.Follower)

env.run()
