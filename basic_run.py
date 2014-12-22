import logging
import entity
import basic_model

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename="log.txt")

logging.info("Starting program")

AGENTS   = 10

env = Environment("basic env")

for i in range(AGENTS):
    env.add_agent(BasicAgent(name="agent" + str(i), goal="Acting up!"))

env.run()

