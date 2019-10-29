from APIServer.api_utils import json_converter, err_return
from indra.env import Env
# these imports below must be automated somehow;
# also, these things are unserializable, NOT unrestorable!
# (Otherwise why bother?)
# also, keep name constant and preface with model name, e.g.,
# fashion[unserializable()]
import models.bacteria as bacteria
import models.bigbox as bigbox
import models.fashion as fashion
import models.flocking as flocking
import models.fmarket as fmarket
import models.gameoflife as gameoflife
import models.sandpile as sandpile
import models.segregation as segregation
import models.wolfsheep as wolfsheep

# this dictionary should be keyed on model id
restore_globals_dict = {
    "Sandpile": sandpile,
    "Petrie dish": bacteria,
    "Town": bigbox,
    "Society": fashion,
    "the_sky": flocking,
    "fmarket": fmarket,
    "A city": segregation,
    "meadow": wolfsheep,
    "Game of Life": gameoflife,
}


def run_model_put(payload, run_time):
    env = Env(name='API env', serial_obj=payload)
    # lookup should be on model id, not env name!
    if env.name not in restore_globals_dict:
        err_return("Model env not found.")
    else:
        restore_globals_dict[env.name].restore_globals(env)

    env.runN(periods=run_time)
    return json_converter(env)
