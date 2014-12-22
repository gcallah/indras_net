import logging
import predator_prey

PRED_LOG = "pred_log.txt"

logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.INFO, filemode='w', filename=PRED_LOG)

logging.info("Starting program")

RABBITS = 4
FOXES   = 2

env = PredPreyEnv("meadow", 50.0, 50.0, logfile=PRED_LOG)

for i in range(FOXES):
    env.add_agent(Fox(name="brer" + str(i), life_force=38.0, 
        repro_age=11, decay_rate=5.8, max_move=40.0, max_detect=80.0,
        rand_age=True))

for i in range(RABBITS):
    env.add_agent(Rabbit(name="bunny" + str(i), life_force=21.8,
        repro_age=3, decay_rate=4.8, max_move=10.0,
        rand_age=True))

entity.Entity.add_universal(Fox, EAT, Rabbit)

env.run()
