from models.basic import main as bamain
from models.basic import set_up as baset_up
from models.basic import agent_action
from models.fashion import main as famain
from models.fashion import set_up as faset_up
from models.fashion import follower_action, common_action, tsetter_action
from models.forestfire import main as ffmain
from models.forestfire import set_up as ffset_up
from models.forestfire import tree_action
from models.sandpile import main as spmain
from models.sandpile import set_up as spset_up
from models.sandpile import sandpile_action, place_action
from models.segregation import main as semain
from models.segregation import set_up as seset_up
from models.segregation import seg_agent_action
from models.scheduler import main as scmain
from models.scheduler import set_up as scset_up
from models.scheduler import sched_agent_action
from models.wolfsheep import main as wsmain
from models.wolfsheep import set_up as wsset_up
from models.wolfsheep import sheep_action, wolf_action


rdict = {
    "basic": bamain,
    "fashion": famain,
    "forestfire": ffmain,
    "sandpile": spmain,
    "scheduler": scmain,
    "segregation": semain,
    "wolfsheep": wsmain,
}

setup_dict = {
    "basic": baset_up,
    "fashion": faset_up,
    "forestfire": ffset_up,
    "sandpile": spset_up,
    "scheduler": scset_up,
    "segregation": seset_up,
    "wolfsheep": wsset_up,
}

action_dict = {
    "agent_action": agent_action,
    "follower_action": follower_action,
    "common_action": common_action,
    "tsetter_action": tsetter_action,
    "tree_action": tree_action,
    "sandpile_action": sandpile_action,
    "place_action": place_action,
    "seg_agent_action": seg_agent_action,
    "sched_agent_action": sched_agent_action,
    "sheep_action": sheep_action,
    "wolf_action": wolf_action
}
