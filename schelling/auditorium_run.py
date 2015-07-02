"""
Set up and run the auditorium model.
"""

import indra.utils as utils
import indra.prop_args as props
import auditorium_model as am

# set up some file names:
MODEL_NM = "auditorium_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.ask("num_agents", "What is num agents?", int, default=16)
    pa.ask("aud_width", "What is auditorium width?", int, default=8)
    pa.ask("aud_height", "What is auditorium height?", int, default=8)

# Now we create a minimal environment for our agents to act within:
env = am.Auditorium("Auditorium",
                    height=pa.get("aud_height"),
                    width=pa.get("aud_width"),
                    torus=False,
                    model_nm=MODEL_NM,
                    num_agents=pa.get("num_agents"))

utils.run_model(env, prog_file, results_file)
