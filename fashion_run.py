import logging
import prop_args as pa
import predator_prey as prdpry
import fashion

MODEL_NM = "fashion"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + "_log.txt"

logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.INFO, filemode='w',
            filename=LOG_FILE)

logging.info("Starting program")

TREND_SETTERS = 20
FOLLOWERS     = 80


pa = pa.PropArgs(PROG_NM)

pa.set("fshn_f_ratio", 1.3)
pa.set("fshn_t_ratio", 1.5)

pa.set("flwr_others", 3)
pa.set("trnd_others", 5)

pa.set("min_adv_periods", 8)


env = SocietyEnv("society", 50.0, 50.0, logfile=LOG_FILE)

for i in range(FOLLOWERS):
    env.add_agent(Follower(name="prole" + str(i),
        max_move=20.0, max_detect=20.0))

for i in range(TREND_SETTERS):
    env.add_agent(TrendSetter(name="hipster" + str(i),
        max_move=20.0, max_detect=20.0))

entity.Entity.add_universal(Follower, prdpry.EAT, TrendSetter)
entity.Entity.add_universal(TrendSetter, prdpry.AVOID, Follower)

env.run()
