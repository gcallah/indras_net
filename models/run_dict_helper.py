from APIServer.model_creator_api import generate_func
from models.bacteria import bacterium_action, toxin_action, nutrient_action
from models.bacteria import create_bacterium
from models.bacteria import create_nutrient
from models.bacteria import create_toxin
from models.bacteria import main as bactmain
from models.bacteria import set_up as bactset_up
from models.basic import agent_action
from models.basic import main as bamain
from models.basic import set_up as baset_up
from models.bigbox import create_consumer
from models.bigbox import main as bbmain
from models.bigbox import set_up as bbset_up
from models.bigbox import town_action, consumer_action, mp_action, bb_action
from capital.capital import create_entr
from capital.capital import create_rholder
from models.coop import create_babysitter
from models.coop import create_central_bank
from models.drunks import create_drinker
from models.drunks import create_non_drinker
from models.ex_boyfriend import create_boyfriend
from models.ex_boyfriend import create_girlfriend
from models.fashion import create_follower
from models.fashion import create_tsetter
from models.fashion import follower_action, common_action, tsetter_action
from models.fashion import main as famain
from models.fashion import set_up as faset_up
from models.flocking import bird_action
from models.flocking import create_bird
from models.fmarket import create_market_maker, plot_asset_price
from models.fmarket import create_trend_follower
from models.fmarket import create_value_investor
from models.fmarket import main as fmmain
from models.fmarket import market_maker_action, trend_follower_action
from models.fmarket import set_up as fmset_up
from models.fmarket import value_investor_action
from models.forestfire import main as ffmain
from models.forestfire import set_up as ffset_up
from models.forestfire import tree_action
from models.gameoflife import create_game_cell
from models.gameoflife import gameoflife_action, game_agent_action
from models.gameoflife import main as gamemain
from models.gameoflife import set_up as gset_up
from models.sandpile import create_grain
from models.sandpile import main as spmain
from models.sandpile import sandpile_action, spagent_action
from models.sandpile import set_up as spset_up
from models.segregation import create_resident
from models.segregation import main as semain
from models.segregation import seg_agent_action
from models.segregation import set_up as seset_up
from models.wolfram import main as wfmain
from models.wolfram import set_up as wfset_up
from models.wolfram import wolfram_action, wfagent_action
from models.wolfsheep import create_sheep
from models.wolfsheep import create_wolf
from models.wolfsheep import main as wsmain
from models.wolfsheep import set_up as wsset_up
from models.wolfsheep import sheep_action, wolf_action

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

# Filled creators_dict partially
# Need to figure out what keys should be assigned to
# create_agent() in different models
creators_dict = {
    "create_resident": create_resident,
    "create_grain": create_grain,
    "create_game_cell": create_game_cell,
    "create_consumer": create_consumer,
    "create_sheep": create_sheep,
    "create_wolf": create_wolf,
    "create_drinker": create_drinker,
    "create_non_drinker": create_non_drinker,
    "create_bird": create_bird,
    "create_boyfriend": create_boyfriend,
    "create_girlfriend": create_girlfriend,
    "create_follower": create_follower,
    "create_tsetter": create_tsetter,
    "create_bacterium": create_bacterium,
    "create_nutrient": create_nutrient,
    "create_toxin": create_toxin,
    "create_babysitter": create_babysitter,
    "create_central_bank": create_central_bank,
    "create_value_investor": create_value_investor,
    "create_market_maker": create_market_maker,
    "create_trend_follower": create_trend_follower,
    "create_entr": create_entr,
    "create_rholder": create_rholder,
}

aux_funcs_dict = {
    "plot_asset_price": plot_asset_price,
}
