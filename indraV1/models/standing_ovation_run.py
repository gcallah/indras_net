#!/usr/bin/env python
"""
This file runs the standing_ovation model.
"""
import indra.prop_args2 as props

MODEL_NM = "standing_ovation"


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.standing_ovation as wsm
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    env = wsm.Auditorium("Auditorium",
                     pa["grid_width"],
                     pa["grid_height"],
                     model_nm=MODEL_NM,
                     preact=True,
                     props=pa)

    num_agents = int(pa["grid_width"] * pa["grid_height"])
    for i in range(num_agents):
        env.add_agent(wsm.Member("member" + str(i), "Enjoying the show", pa["noise_level"]))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
