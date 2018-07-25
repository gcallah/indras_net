#!/usr/bin/env python3
"""
A script that runs big_box_model. It simulates the market economy
of consumers, mom and pops, and big boxes.
"""
MODEL_NM = "bigbox"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.prop_args as props
import bigbox as bb

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
    # Now we create a town for our agents to act in:
    env = bb.EverytownUSA(pa["grid_width"],
                          pa["grid_height"],
                          model_nm=MODEL_NM,
                          props=pa)
    # Now we loop creating multiple agents with numbered names
    # based on the number of agents of that type to create:
    for i in range(pa["num_consumers"]):
        env.add_agent(bb.Consumer("consumer" + str(i),
                                  goal=(i % bb.NUM_GOODS),
                                  init_state=0,
                                  allowance=pa["allowance"]))
        
    for i in range(pa["num_mom_and_pops"]):
        env.add_agent(bb.MomAndPop("mom_and_pop" + str(i),
                                   goal=(i % bb.NUM_GOODS),
                                   endowment=pa["endowment"],
                                   expenses=pa["expenses"],
                                   adj=pa["pref_for_mp"]
                                   ))
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
