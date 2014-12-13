import logging
import predator_prey as prdpry
import fashion

LOG_FILE = "fashion_log.txt"

logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.INFO, filemode='w',
            filename=LOG_FILE)

logging.info("Starting program")

TREND_SETTERS = 20
FOLLOWERS     = 60

env = SocietyEnv("society", 50.0, 50.0, logfile=LOG_FILE)

for i in range(FOLLOWERS):
    env.add_agent(Follower(name="prole" + str(i),
        life_force=20.0, repro_age=1000.0, decay_rate=0.0,
        max_move=4.0, max_detect=12.0))

for i in range(TREND_SETTERS):
    env.add_agent(TrendSetter(name="hipster" + str(i),
        life_force=20.0, repro_age=1000.0, decay_rate=0.0,
        max_move=4.0, max_detect=12.0))

entity.Entity.add_universal(Follower, prdpry.EAT, TrendSetter)
entity.Entity.add_universal(TrendSetter, prdpry.AVOID, Follower)

env.run()
