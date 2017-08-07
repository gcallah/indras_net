#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""

import indra.utils as utils
import indra.prop_args as props
import models.menu_model as mm

# set up some file names:
MODEL_NM = "menu_model"

def run():
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store menu parameters in a
    # "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    pa = utils.read_props(MODEL_NM)
    if pa is None:
        pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
        pa.set("num_agents", 10)
    
    # Now we create a minimal environment for our agents to act within:
    env = mm.MenuEnv(model_nm=MODEL_NM, props=pa)
    
    # Now we loop creating multiple agents
    #  with numbered names based on the loop variable:
    for i in range(pa.get("num_agents")):
        env.add_agent(mm.MenuAgent(name="agent" + str(i),
                                   goal="testing our menu capabilities!"))
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
