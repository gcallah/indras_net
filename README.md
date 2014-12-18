Indra
=====

This is a project building an agent-based modeling system in Python. The ultimate goal is to build a GUI front-end that will allow non-coders to build models, while at the same time permitting coders to use Python for more flexibility in model creation.

basic_run.py creates a barebones environment of agents that just print their names. It can be the basis for your own run file.

entity.py contains the basic agent class, and basic environment, as well as some plumbing for connecting them.

fashion.py is Adam Smith's fashion model. fashion_run.py sets some parameters, and then runs the model.

height.py is Thomas Schelling's genetic engineered height model. height_run.py runs the model.

predator_prey.py is the core of a family of predator prey models, of which Smith's fashion model is the first. pred-run.py runs this model.

spatial_agent.py contains an agent sub-class and environment sub-class that position agents in space.
