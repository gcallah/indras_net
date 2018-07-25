#!/usr/bin/env python3
"""
Runs a financial market model with value investors and chart followers.
"""
MODEL_NM = "fmarket"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.prop_args as props
import models.fmarket as fm

# set up some file names:

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a "property" file; this allows us to save
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

    # Now we create a asset environment for our agents to act within:
    env = fm.FinMarket("Financial Market",
                       pa["grid_height"],
                       pa["grid_width"],
                       torus=False,
                       model_nm=MODEL_NM,
                       props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    for i in range(pa["num_followers"]):
        env.add_agent(fm.ChartFollower("follower" + str(i),
                                       "Following trend",
                                       pa["fmax_move"],
                                       pa["variability"]))
    for i in range(pa["num_vinvestors"]):
        env.add_agent(fm.ValueInvestor("value_inv" + str(i), "Buying value",
                                       pa["vmax_move"],
                                       pa["variability"]))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
