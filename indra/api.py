# define the API for our Indra server.

import indra.env
from indra.entity import Agent

TEST_GOAL = "Testing the API"

def get_agent(agent_id):
    agent = Agent("test_agent", TEST_GOAL)
    return agent.to_json()


