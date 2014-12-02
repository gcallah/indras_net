import logging
import entity

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, filemode='w', filename="log.txt")

logging.info("Starting program")

AGENTS   = 10

env = Environment("meadow")

for i in range(AGENTS):
    env.add_agent(Agent(name="agent" + str(i)))

env.run()
