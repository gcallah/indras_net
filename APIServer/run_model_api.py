from APIServer.api_utils import json_converter, err_return
from indra.env import Env
# these imports below must be automated somehow;
# also, these things are unserializable, NOT unrestorable!
# (Otherwise why bother?)
# also, keep name constant and preface with model name, e.g.,
# fashion[unserializable()]
from models.sandpile import sp_unrestorable
from models.bacteria import bt_unrestorable
from models.bigbox import bb_unrestorable
from models.fashion import fs_unrestorable
from models.flocking import fl_unrestorable
from models.fmarket import fm_unrestorable
from models.segregation import sg_unrestorable
from models.wolfsheep import ws_unrestorable
from models.gameoflife import gl_unrestorable


def run_model_put(payload, run_time):
    env = Env(name='API env', serial_obj=payload)
    # this should be dictionary lookup not if elif statements!
    # furthermore, lookup should be on model id, not env name!
    if env.name == "Sandpile":
        sp_unrestorable(env)
    elif env.name == "Petrie dish":
        bt_unrestorable(env)
    elif env.name == "Town":
        bb_unrestorable(env)
    elif env.name == "Society":
        fs_unrestorable(env)
    elif env.name == "the_sky":
        fl_unrestorable(env)
    elif env.name == "fmarket":
        fm_unrestorable(env)
    elif env.name == "A city":
        sg_unrestorable(env)
    elif env.name == "meadow":
        ws_unrestorable(env)
    elif env.name == "Game of Life":
        gl_unrestorable(env)
    else:
        err_return("Model env not found.")

    env.runN(periods=run_time)
    return json_converter(env)
