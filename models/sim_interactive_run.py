import indra.prop_args2 as props
import os

MODEL_NM = "sim_interactive"

<<<<<<< HEAD
=======

>>>>>>> 71cbb6374957a716fc9a0c5661862edf2e6c609b
def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)

    import indra.utils as utils
    import models.sim_interactive as sm

    # set up some file names:
<<<<<<< HEAD
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
=======
    (prog_file, log_file, prop_file,
     results_file) = utils.gen_file_names(MODEL_NM)
>>>>>>> 71cbb6374957a716fc9a0c5661862edf2e6c609b
    # We store basic parameters in a "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.

    if pa["user_type"] == props.WEB:
        pa["base_dir"] = os.environ['base_dir']

    # Now we create an environment for our agents to act within:
    env = sm.SimInteractiveEnv("",
<<<<<<< HEAD
                      pa["grid_width"],
                      pa["grid_height"],
                      model_nm=pa.model_nm,
                      props=pa)
=======
                               pa["grid_width"],
                               pa["grid_height"],
                               model_nm=pa.model_nm,
                               props=pa)
>>>>>>> 71cbb6374957a716fc9a0c5661862edf2e6c609b

    # create given number of agents
    env.add_agent()

    return utils.run_model(env, prog_file, results_file)

<<<<<<< HEAD
if __name__ == "__main__":
    run()
=======

if __name__ == "__main__":
    run()
>>>>>>> 71cbb6374957a716fc9a0c5661862edf2e6c609b
