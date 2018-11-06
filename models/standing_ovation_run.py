#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""
MODEL_NM = "standing_ovation"

import random
import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import models.standing_ovation as stov

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    global pa
    num_agents = pa["grid_width"] * pa["grid_height"]
    num_agents = 25 #Temporary test value, replace with width * height

    env = stov.Auditorium(
                    pa["grid_width"],
                    pa["grid_height"],
                    model_nm=MODEL_NM,
                    props=pa
                    )
    #Generate audience members
    for i in range(num_agents):
        noise = random.uniform(0.7,9.0)
        env.add_agent(stov.AudienceAgent("Member" + str(i), "Enjoying the show", pa["noise_level"]))
    ##Saving these in case I have to test this
    # # test prop_args as an iterable:
    # for prop, val in pa.items():
    #     print(prop + ": " + str(val))
    #
    # # test that props work as a dictionary:
    # if "num_agents" in pa:
    #     print("In is working!")
    #
    # # test what pa["num_agents"] is:
    # num_agents = pa["num_agents"]
    # print("num_agents = " + str(num_agents))
    #
    # # make sure we can get props length:
    # print("Props length = " + str(len(pa)))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
