#!/usr/bin/env python3
"""
predprey_run.py
Script to run our predator-prey model.
"""
import indra.utils as utils
import indra.node as node
import indra.prop_args as props
import predprey_model as ppm


MODEL_NM = "predprey_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_foxes", 16)
    pa.set("num_rabbits", 48)
    pa.set("num_zombies", 6)
    pa.set("fox_repro_age", 11)
    pa.set("rabbit_repro_age", 3.6)
    pa.set("fox_life_force", 32.8)
    pa.set("rabbit_life_force", 22.0)
    pa.set("fox_max_move", 12.8)
    pa.set("rabbit_max_move", 10.2)
    pa.set("fox_decay_rate", 5.8)
    pa.set("rabbit_decay_rate", 3.98)
    pa.set("fox_max_detect", 40.0)

env = ppm.PredPreyEnv("meadow", 50.0, 50.0)

for i in range(pa.get("num_foxes")):
    env.add_agent(ppm.Fox(name="brer" + str(i),
                          life_force=pa.get("fox_life_force"),
                          repro_age=pa.get("fox_repro_age"),
                          decay_rate=pa.get("fox_decay_rate"),
                          max_move=pa.get("fox_max_move"),
                          max_detect=pa.get("fox_max_detect"),
                          rand_age=True))

for i in range(pa.get("num_rabbits")):
    env.add_agent(ppm.Rabbit(name="bunny" + str(i),
                             life_force=pa.get("rabbit_life_force"),
                             repro_age=pa.get("rabbit_repro_age"),
                             decay_rate=pa.get("rabbit_decay_rate"),
                             max_move=pa.get("rabbit_max_move"),
                             goal=ppm.EAT,
                             rand_age=True))

# for i in range(20):
#     env.add_agent(ppm.Grass("grass" + str(i), 100.0, 10.0, 10.0))

node.add_prehension(ppm.Fox, ppm.EAT, ppm.Rabbit)
node.add_prehension(ppm.Rabbit, ppm.AVOID, ppm.Fox)
# node.add_prehension(ppm.Rabbit, ppm.EAT, ppm.Grass)

utils.run_model(env, prog_file, results_file)
