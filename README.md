# Indra

[![Build Status](https://travis-ci.com/gcallah/indras_net.svg?branch=master)](https://travis-ci.com/gcallah/indras_net)

This is a project building an agent-based modeling system in Python. The ultimate goal is to build a GUI front-end that will allow non-coders to build models, while at the same time permitting coders to use Python for more flexibility in model creation.

**NOTE**: We have established a standard for models and parameter files that run them. For model X, we should have:

- `X_model.py`: implements the model
- `X_run.py`: runs it

## FILE LIST:

**In Indra, the core of the system:**

- `agent_pop.py` maintains our agent population. It permits backwards, forwards, and random iteration over our population of agents, as well as iteration over agents of a single type. It also maintains a population history for every agent type.
- `entity.py` contains the basic agent class, and basic environment, as well as some plumbing for connecting them.
- `menu.py` contains our basic menuing code.
- `node.py` is the root of all the other objects in our system. Its purpose is to make the whole system graphable.
- `prop_args.py` is the start of a property manager.
- `spatial_agent.py` contains an agent sub-class for agents that will be positioned in space.
- `spatial_env.py` constructs a complex plane for agents to move on, and tracks where they are.

**In models, various models using this core:**
- `barter_model.py` extends `edgebox_model.py` to include multiple (rather than just two) agents. `barter_run.py` runs this model.
- `basic_model.py` is an simple agent and environment. Cloning this allows you to get going more easily.
- `basic_run.py` creates a barebones environment of agents that just print their names. It can be the basis for your own run file.
- `coop_model.py` implements the babysitting co-op model Paul Krugman made famous. `coop_run.py` runs this model.
- `edgebox_model.py` implements the "Edgeworth Box" model of exchange from economics. `edgebox_run.py` runs this model.
- `emp_model.py` and `emp_run.py` are some experiments with agent heirarchies.
- `fashion_model.py` is Adam Smith's fashion model.
- `fashion_run.py` sets some parameters for `fashion_model.py` and then runs the model.
- `height_model.py` is Thomas Schelling's genetic engineered height model. `height_run.py` runs the model.
- `menger_model.py` is the beginnings of an attempt to get money to emerge in a market. `menger_run.py` runs this model.
- `menu_model.py` and `menu_run.py` exist to test the menu system in isolation.
- `predator_prey.py` is the core of a family of predator prey models, of which Smith's fashion model is the first descendant model. `pred_run.py` runs this model.
- `timer_model.py` exists to allow timing of isolated portions of our code. `timer_run.py` runs this model.
