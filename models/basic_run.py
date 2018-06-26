#!/Users/gcallah/miniconda3/bin/python
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""

import indra.prop_args as props
import indra.utils as utils
import models.basic_model as bm

# set up some file names:
MODEL_NM = "Basic"


def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    # We store basic parameters in a
    # "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.

    # TODO: Place this logic in prop_args
    if prop_dict is not None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=prop_dict)
    elif utils.read_props(MODEL_NM):
        pa = utils.read_props(MODEL_NM)
    else:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)

    # Now we create a minimal environment for our agents to act within:
    env = bm.BasicEnv(model_nm=MODEL_NM, props=pa)

    # Now we loop creating multiple agents
    #  with numbered names based on the loop variable:
    for i in range(pa.get("num_agents")):
        env.add_agent(bm.BasicAgent(name="agent" + str(i),
                                    goal="acting up!"))

    utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
