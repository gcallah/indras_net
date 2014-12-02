import logging
import entity
import predator_prey

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename="log.txt")

logging.info("Starting program")

RABBITS = 80
FOXES   = 20

env = PredPreyEnv("meadow", 50.0, 50.0)

for i in range(RABBITS):
    env.add_creature(Rabbit(name="bunny" + str(i), life_force=21.8, 
        repro_age=3, decay_rate=4.3, max_move=10.0, rand_age=True))

for i in range(FOXES):
    env.add_creature(Fox(name="brer" + str(i), life_force=38.0, 
        repro_age=11, decay_rate=5.2, max_move=20.0, max_detect=40.0,
        rand_age=True))

entity.Entity.add_universal(Fox, EAT, Rabbit)

env.run()
