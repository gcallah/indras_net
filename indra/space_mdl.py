"""
space_mdl.py:
Setup an interesting interactive, spatial env in which to play
and try out new features.
We're going to do "bad" import *s here because this isn't "real"
code, just a playground for experimenting.
"""

from agent import Agent
from space import Space, distance

DEF_AGENTS = 4


def spatial_agent_act(agent):
    if agent.locator:
        agent.locator.place_member(agent)
        print("I'm " + agent.name + " and I'm at: " + str(agent.pos))


st = Space("Space test")
for i in range(DEF_AGENTS):
    st += Agent("sa" + str(i), action=spatial_agent_act)

print("Distance between sa0 and sa1 is "
      + str(distance(st["sa0"], st["sa1"])))
