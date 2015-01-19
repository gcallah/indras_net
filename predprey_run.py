import logging
import node
import prop_args as props
import entity as ent
import predprey_model as ppm


MODEL_NM = "predprey_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "predprey.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_foxes", 12)
    pa.set("num_rabbits", 80)
    pa.set("fox_repro_age", 11)
    pa.set("rabbit_repro_age", 3.6)
    pa.set("fox_life_force", 38.8)
    pa.set("rabbit_life_force", 23)
    pa.set("fox_max_move", 38.8)
    pa.set("rabbit_max_move", 10.2)
    pa.set("fox_decay_rate", 5.8)
    pa.set("rabbit_decay_rate", 3.98)
    pa.set("fox_max_detect", 60.0)

env = ppm.PredPreyEnv("meadow", 50.0, 50.0)
pa.set("env", env)

for i in range(pa.get("num_foxes")):
    env.add_agent(ppm.Fox(name="brer" + str(i),
        life_force=pa.get("fox_life_force"), 
        repro_age=pa.get("fox_repro_age"),
        decay_rate=pa.get("fox_decay_rate"),
        max_move=pa.get("fox_max_move"),
        max_detect=pa.get("fox_max_detect"),
        rand_age=True))

for i in range(pa.get("num_rabbits")):
    env.add_agent(ppm.Rabbit(name="bunny" + str(i),
        life_force=pa.get("rabbit_life_force"),
        repro_age=pa.get("rabbit_repro_age"),
        decay_rate=pa.get("rabbit_decay_rate"),
        max_move=pa.get("rabbit_max_move"),
        rand_age=True))

node.add_prehension(ppm.Fox, ppm.EAT, ppm.Rabbit)

logging.info("Starting program")
env.run()

