#!/usr/bin/env python3

import indra.prop_args2 as props
import os
import random

MODEL_NM = "sim_interactive"


# number of cars
# slow car speed
# acceleration
# deceleration


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.sim_interactive as sm

    # set up some file names:
    (prog_file, log_file, prop_file,
     results_file) = utils.gen_file_names(MODEL_NM)
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.

    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ['base_dir']

    # Now we create an environment for our agents to act within:
    env = sm.SimInteractiveEnv("Car_sim",
                               pa["grid_width"],
                               pa["grid_height"],
                               model_nm=MODEL_NM,
                               props=pa)

    # create given number of slow vehicles
    # print(sm)
    max_speed = pa["max_speed"]
    min_speed = pa["min_speed"]

    # East bound cars
    for i in range(pa["slow_car_num"]):
        newAgent = sm.EastCar('Vehicle #' + str(i),
                              random.randint(min_speed, max_speed))
        env.add_agent(newAgent)
        env.move(newAgent, i + 2, env.height // 2)

    # South bound cars
    num_north_cars = pa["slow_car_num"]
    for i in range(pa["fast_car_num"]):
        newAgent = sm.SouthCar('Vehicle #' + str(i + num_north_cars),
                               random.randint(min_speed, max_speed))
        env.add_agent(newAgent)
        env.move(newAgent, env.width // 2, env.height - (i + 2))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
