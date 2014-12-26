import sys
import logging
import prop_args as pa
import entity
import edgebox_model

MODEL_NM = "edgebox_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename=LOG_FILE)

logging.info("Starting program")

for i in range(len(sys.argv)):
    print(sys.argv[i])

props = pa.PropArgs(MODEL_NM)

props.set("logfile", LOG_FILE)


# props = pa.PropArgs.read_props(MODEL_NM, "edgebox_props.txt")

env = EdgeboxEnv(model_nm=MODEL_NM)

env.add_agent(EdgeboxAgent(name="Albert"))
env.add_agent(EdgeboxAgent(name="Beatrice"))

env.run()

