"""
This file runs the standing_ovation model.
"""
import indra.prop_args2 as props
#import os

MODEL_NM = "standing_ovation"

def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.standing_ovation as stov
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    width = pa["grid_width"]
    height = pa["grid_height"]
    #noise = pa["noise"]

    # #for testing, delete the following 2 assignments once done
    # width = 5
    # height = 5

    num_agents = int(width * height)

    env = stov.Auditorium(width,
                       height,
                       #noise,
                       model_nm=MODEL_NM,
                       torus=False,
                       props=pa)

    for i in range(num_agents):
        env.add_agent(stov.AudienceAgent("Member" + str(i), "Enjoying the show"))
    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()