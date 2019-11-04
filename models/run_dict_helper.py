from models.bacteria import bacterium_action, toxin_action, nutrient_action
from models.bacteria import main as bactmain
from models.bacteria import set_up as bactset_up
from models.basic import agent_action
from models.basic import main as bamain
from models.basic import set_up as baset_up
from models.bigbox import main as bbmain
from models.bigbox import set_up as bbset_up
from models.bigbox import town_action, consumer_action, mp_action, bb_action
from models.fashion import follower_action, common_action, tsetter_action
from models.fashion import main as famain
from models.fashion import set_up as faset_up
from models.flocking import bird_action
from models.fmarket import main as fmmain
from models.fmarket import market_maker_action, trend_follower_action
from models.fmarket import set_up as fmset_up
from models.fmarket import value_investor_action
from models.forestfire import main as ffmain
from models.forestfire import set_up as ffset_up
from models.forestfire import tree_action
from models.gameoflife import gameoflife_action, game_agent_action
from models.gameoflife import main as gamemain
from models.gameoflife import set_up as gset_up
from models.sandpile import main as spmain
from models.sandpile import sandpile_action, spagent_action
from models.sandpile import set_up as spset_up
from models.segregation import main as semain
from models.segregation import seg_agent_action
from models.segregation import set_up as seset_up
from models.wolfram import main as wfmain
from models.wolfram import set_up as wfset_up
from models.wolfram import wolfram_action, wfagent_action
from models.wolfsheep import main as wsmain
from models.wolfsheep import set_up as wsset_up
from models.wolfsheep import sheep_action, wolf_action
from APIServer.model_creator_api import generate_func

rdict = {
    "basic": bamain,
    "fashion": famain,
    "forestfire": ffmain,
    "sandpile": spmain,
    "segregation": semain,
    "wolfsheep": wsmain,
    "bacteria": bactmain,
    "bigbox": bbmain,
    "gameoflife": gamemain,
    "wolfram": wfmain,
    "fmarket": fmmain,
}

setup_dict = {
    "basic": baset_up,
    "fashion": faset_up,
    "forestfire": ffset_up,
    "sandpile": spset_up,
    "segregation": seset_up,
    "wolfsheep": wsset_up,
    "bacteria": bactset_up,
    "gameoflife": gset_up,
    "bigbox": bbset_up,
    "wolfram": wfset_up,
    "fmarket": fmset_up,
}

action_dict = {
    "agent_action": agent_action,
    "follower_action": follower_action,
    "common_action": common_action,
    "tsetter_action": tsetter_action,
    "tree_action": tree_action,
    "sandpile_action": sandpile_action,
    "spagent_action": spagent_action,
    "seg_agent_action": seg_agent_action,
    "sheep_action": sheep_action,
    "wolf_action": wolf_action,
    "bacterium_action": bacterium_action,
    "toxin_action": toxin_action,
    "nutrient_action": nutrient_action,
    "town_action": town_action,
    "consumer_action": consumer_action,
    "mp_action": mp_action,
    "bb_action": bb_action,
    "gameoflife_action": gameoflife_action,
    "game_agent_action": game_agent_action,
    "wolfram_action": wolfram_action,
    "wfagent_action": wfagent_action,
    "market_maker_action": market_maker_action,
    "trend_follower_action": trend_follower_action,
    "value_investor_action": value_investor_action,
    "bird_action": bird_action,
    "generate_func": generate_func
}
