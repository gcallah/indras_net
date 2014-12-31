import logging
import prop_args as props
import entity
import basic_model

MODEL_NM = "basic_model"
PROG_NM  = MODEL_NM + ".py"
LOG_FILE = MODEL_NM + ".txt"

read_props = False

if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, "basic.props")
else:
    pa = props.PropArgs(MODEL_NM, logfile=LOG_FILE)
    pa.set("num_agents", 12)

logging.info("Starting program " + PROG_NM)

env = BasicEnv(model_nm=MODEL_NM)

for i in range(pa.get("num_agents")):
    env.add_agent(BasicAgent(name="agent" + str(i), goal="acting up!"))

env.run()

