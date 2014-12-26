import logging
import prop_args as pa
import predprey_model as prdpry
import fashion_model

MODEL_NM = "fashion"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + "_log.txt"

logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.INFO, filemode='w',
            filename=LOG_FILE)

logging.info("Starting program")


pa = pa.PropArgs(MODEL_NM)

pa.set("num_trndstr", 20)
pa.set("num_flwr", 80)

pa.set("fshn_f_ratio", 1.3)
pa.set("fshn_t_ratio", 1.5)

pa.set("flwr_others", 3)
pa.set("trnd_others", 5)

pa.set("min_adv_periods", 8)

pa.set("logfile", LOG_FILE)


env = SocietyEnv("society", 50.0, 50.0, model_nm=MODEL_NM)

for i in range(pa.get("num_flwr")):
    env.add_agent(Follower(name="prole" + str(i),
        max_move=20.0, max_detect=20.0))

for i in range(pa.get("num_trndstr")):
    env.add_agent(TrendSetter(name="hipster" + str(i),
        max_move=20.0, max_detect=20.0))

entity.Entity.add_universal(Follower, prdpry.EAT, TrendSetter)
entity.Entity.add_universal(TrendSetter, prdpry.AVOID, Follower)

env.run()
