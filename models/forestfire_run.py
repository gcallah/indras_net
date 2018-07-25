#!/usr/bin/env python3
"""
This file runs the forestfire_model.
"""
MODEL_NM = "forestfire"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import models.forestfire as fm

# set up some file names:


def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a
    # "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    global pa

    if prop_dict is not None:
        prop_dict[props.PERIODS] = 1
        pa.add_props(prop_dict)
    else:
        result = utils.read_props(MODEL_NM)
        if result:
            pa.add_props(result.props)
        else:
            utils.ask_for_params(pa)
    
    density = pa["density"]
    grid_x = pa["grid_width"]
    grid_y = pa["grid_height"]
    
    # Now we create a forest environment for our agents to act within:
    env = fm.ForestEnv(grid_x, grid_y, density, pa["strike_freq"],
                       pa["regen_period"],
                       model_nm=MODEL_NM, torus=False,
                       props=pa)
    
    num_agents = int(grid_x * grid_y * density)
    
    for i in range(num_agents):
        env.add_agent(fm.Tree(name="tree" + str(i)))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
