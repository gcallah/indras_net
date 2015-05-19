"""
Set up and run the auditorium model.
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import auditorium_model as am

# set up some file names:
MODEL_NM = "auditorium_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 16)
    pa.set("aud_width", 8)
    pa.set("aud_height", 8)

# Now we create a minimal environment for our agents to act within:
env = am.Auditorium("Auditorium",
                    height=pa.get("aud_height"),
                    width=pa.get("aud_width"),
                    torus=False,
                    model_nm=MODEL_NM,
                    num_agents=pa.get("num_agents"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
env.run()
env.record_results(results_file)
