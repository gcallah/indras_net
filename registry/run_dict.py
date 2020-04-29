"""
The file to register functions we need to restore at run time.
"""
from models.bacteria import bacterium_action, toxin_action, nutrient_action
from models.bacteria import main as bactmain
from models.bacteria import set_up as bactset_up
from models.basic import agent_action
from models.basic import main as bamain
from models.basic import set_up as baset_up
from models.el_farol import main as efmain
from models.el_farol import set_up as efset_up
from models.el_farol import drinker_action
from models.fashion import main as famain
from models.fashion import set_up as faset_up
from models.fashion import follower_action, common_action, tsetter_action
from models.fmarket import main as fmmain
from models.fmarket import market_maker_action, trend_follower_action
from models.fmarket import set_up as fmset_up
from models.fmarket import value_investor_action
from models.forestfire import main as ffmain
from models.forestfire import set_up as ffset_up
from models.forestfire import tree_action
from models.segregation import main as segmain
from models.segregation import set_up as segset_up
from models.segregation import seg_agent_action
from models.wolfsheep import main as wsmain
from models.wolfsheep import set_up as wsset_up
from models.wolfsheep import sheep_action, wolf_action
from models.wolfsheep import create_sheep, create_wolf
from capital.money import main as mnmain
from capital.money import set_up as mnset_up
from capital.money import trader_action as mntrader_action

rdict = {
    "basic": bamain,
    "bacteria": bactmain,
    "el_farol": efmain,
    "fashion": famain,
    "fmarket": fmmain,
    "forestfire": ffmain,
    "segregation": segmain,
    "wolfsheep": wsmain,
    "money": mnmain,
}

setup_dict = {
    "basic": baset_up,
    "bacteria": bactset_up,
    "el_farol": efset_up,
    "fashion": faset_up,
    "fmarket": fmset_up,
    "forestfire": ffset_up,
    "segregation": segset_up,
    "wolfsheep": wsset_up,
    "money": mnset_up,
}

action_dict = {
    "agent_action": agent_action,
    "bacterium_action": bacterium_action,
    "common_action": common_action,
    "drinker_action": drinker_action,
    "follower_action": follower_action,
    "market_maker_action": market_maker_action,
    "nutrient_action": nutrient_action,
    "sheep_action": sheep_action,
    "wolf_action": wolf_action,
    "toxin_action": toxin_action,
    "seg_agent_action": seg_agent_action,
    "tsetter_action": tsetter_action,
    "tree_action": tree_action,
    "trend_follower_action": trend_follower_action,
    "value_investor_action": value_investor_action,
    "money_action": mntrader_action,
}


member_creator_dict = {
    "create_sheep": create_sheep,
    "create_wolf": create_wolf,
}
