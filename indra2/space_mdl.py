"""
space_mdl.py:
Setup an interesting interactive, spatial env in which to play
and try out new features.
We're going to do "bad" import *s here because this isn't "real"
code, just a playground for experimenting.
"""

from agent import Agent
from space import Space, DEF_WIDTH, DEF_HEIGHT  # , distance

DEF_AGENTS = 4


def spatial_agent_act(agent):
    if agent.locator:
        agent.locator.place_member(agent)
        print("I'm " + agent.name + " and I'm at: " + str(agent.pos))


st = Space("Space test", DEF_WIDTH, DEF_HEIGHT)
for i in range(DEF_AGENTS):
    st += Agent("space_agent" + str(i), action=spatial_agent_act)
