import logging
import predator_prey


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename="log.txt")

logging.info("Starting program")

RABBITS = 12
FOXES   = 6

env = PredPreyEnv("meadow", 50.0, 50.0)

for i in range(FOXES):
    env.add_agent(Fox(name="brer" + str(i), life_force=39.0, 
        repro_age=10, decay_rate=5.6, max_move=40.0, max_detect=60.0,
        rand_age=True))

for i in range(RABBITS):
    env.add_agent(Rabbit(name="bunny" + str(i), life_force=21.6, 
        repro_age=3, decay_rate=5.0, max_move=10.0,
        rand_age=True))

entity.Entity.add_universal(Fox, EAT, Rabbit)

env.run()
