import logging
import predator_prey as prdpry
import fashion


logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.INFO, filemode='w',
            filename="fashion_log.txt")

logging.info("Starting program")

TREND_SETTERS = 2
FOLLOWERS     = 4

env = SocietyEnv("society", 50.0, 50.0)

for i in range(FOLLOWERS):
    env.add_agent(Follower(name="prole" + str(i),
        life_force=20.0, repro_age=1000.0, decay_rate=0.0,
        max_move=10.0, max_detect=16.0))

for i in range(TREND_SETTERS):
    env.add_agent(TrendSetter(name="hipster" + str(i),
        life_force=20.0, repro_age=1000.0, decay_rate=0.0,
        max_move=4.0))

entity.Entity.add_universal(Follower, prdpry.EAT, TrendSetter)

env.run()
