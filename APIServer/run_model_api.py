from APIServer.api_utils import json_converter, err_return
from indra.env import Env
# these imports below must be automated somehow;
# also, these things are unserializable, NOT unrestorable!
# (Otherwise why bother?)
# also, keep name constant and preface with model name, e.g.,
# fashion[unserializable()]
from models.bacteria import bt_unrestorable
from models.bigbox import bb_unrestorable
import models.fashion as fashion
from models.flocking import fl_unrestorable
from models.fmarket import fm_unrestorable
from models.gameoflife import gl_unrestorable
from models.sandpile import sp_unrestorable
from models.segregation import sg_unrestorable
from models.wolfsheep import ws_unrestorable

# this dictionary should be keyed on model id
restore_globals_dict = {
    "Sandpile": sp_unrestorable,
    "Petrie dish": bt_unrestorable,
    "Town": bb_unrestorable,
    "Society": fashion.restore_globals,
    "the_sky": fl_unrestorable,
    "fmarket": fm_unrestorable,
    "A city": sg_unrestorable,
    "meadow": ws_unrestorable,
    "Game of Life": gl_unrestorable,
}


def run_model_put(payload, run_time):
    env = Env(name='API env', serial_obj=payload)
    # lookup should be on model id, not env name!
    if env.name not in restore_globals_dict:
        err_return("Model env not found.")
    else:
        restore_globals_dict[env.name](env)

    env.runN(periods=run_time)
    return json_converter(env)
