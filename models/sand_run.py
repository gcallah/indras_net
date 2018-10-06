#!/usr/bin/env python3
"""
A script to test our grid capabilities.
"""
import indra.prop_args2 as props

MODEL_NM = "sand"


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.sand as sm
    # set up some file names:
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # Now we create a minimal environment for our agents to act within:
    env = sm.SandEnv("Abelian sand env",
                     pa["grid_width"],
                     pa["grid_height"],
                     model_nm=MODEL_NM,
                     props=pa)
    
    # This env adds agents itself.
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
