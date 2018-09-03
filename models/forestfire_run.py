#!/usr/bin/env python3
"""
This file runs the forestfire_model.
"""
MODEL_NM = "forestfire"

import indra.prop_args2 as props
import os

# set up some file names:


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.forestfire as fm
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ["base_dir"]
    
    grid_x = pa["grid_width"]
    grid_y = pa["grid_height"]
    density = pa["density"]

    # Now we create a forest environment for our agents to act within:
    env = fm.ForestEnv(grid_x,
                       grid_y,
                       density,
                       pa["strike_freq"],
                       pa["regen_period"],
                       model_nm=MODEL_NM,
                       torus=False,
                       props=pa)
    
    num_agents = int(grid_x * grid_y * density)
    
    for i in range(num_agents):
        env.add_agent(fm.Tree(name="tree" + str(i)))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
