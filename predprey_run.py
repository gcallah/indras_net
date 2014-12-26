import logging
import prop_args as pa
import predprey_model

MODEL_NM = "predprey_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + "_log.txt"

logging.basicConfig(format='%(levelname)s:%(message)s',
            level=logging.INFO, filemode='w', filename=PRED_LOG)

logging.info("Starting program")

pa = pa.PropArgs(MODEL_NM)
pa.set("num_foxes", 2)
pa.set("num_rabbits", 4)
pa.set("logfile", LOG_FILE)

env = PredPreyEnv("meadow", 50.0, 50.0)

for i in range(pa.get("num_foxes")):
    env.add_agent(Fox(name="brer" + str(i), life_force=38.0, 
        repro_age=11, decay_rate=5.8, max_move=40.0, max_detect=80.0,
        rand_age=True))

for i in range(pa.get("num_rabbits")):
    env.add_agent(Rabbit(name="bunny" + str(i), life_force=21.8,
        repro_age=3, decay_rate=4.8, max_move=10.0,
        rand_age=True))

entity.Entity.add_universal(Fox, EAT, Rabbit)

env.run()
