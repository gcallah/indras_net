#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""


import indra.prop_args2 as props

MODEL_NM = "basic"


def run(prop_dict=None):
    # We need to create props before we import the basic model,
    # as our choice of display_method is dependent on the user_type.

    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import models.basic as bm
    import indra.utils as utils
    (prog_file, log_file, prop_file,
     results_file) = utils.gen_file_names(MODEL_NM)

    # test prop_args as an iterable:
    for prop, val in pa.items():
        print(prop + ": " + str(val))

    # test that props work as a dictionary:
    if "num_agents" in pa:
        print("In is working!")

    # test what pa["num_agents"] is:
    num_agents = pa["num_agents"]
    print("num_agents = " + str(num_agents))

    # make sure we can get props length:
    print("Props length = " + str(len(pa)))

    # Now we create a minimal environment for our agents to act within:
    env = bm.BasicEnv(model_nm=MODEL_NM, props=pa)

    # Now we loop creating multiple agents
    #  with numbered names based on the loop variable:
    for i in range(num_agents):
        env.add_agent(bm.BasicAgent(name="agent" + str(i),
                                    goal="acting up!"))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
