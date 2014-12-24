import sys
import logging
import prop_args as pa
import entity
import basic_model

MODEL_NM = "basic_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename=LOG_FILE)

logging.info("Starting program")

for i in range(len(sys.argv)):
    print(sys.argv[i])

# props = pa.PropArgs(MODEL_NM)

# props.set("num_agents", 12)

props = pa.PropArgs.read_props(MODEL_NM, "basic_props.txt")

env = BasicEnv(model_nm=MODEL_NM)

for i in range(props.get("num_agents")):
    env.add_agent(BasicAgent(name="agent" + str(i), goal="acting up!"))

env.run()

