"""
The file to register functions we need to restore at run time.
"""
from models.bacteria import bacterium_action, toxin_action, nutrient_action
from models.bacteria import set_up as bactset_up
from models.bacteria import MODEL_NAME as BAMODEL_NAME
from models.basic import agent_action
from models.basic import set_up as baset_up
from models.basic import MODEL_NAME as BSMODEL_NAME
from models.coop import babysitter_action, coop_action, central_bank_action
from models.coop import set_up as coset_up
from models.coop import MODEL_NAME as COMODEL_NAME
from models.coop import set_env_attrs as co_set_env_attrs
from models.el_farol import set_up as efset_up
from models.el_farol import drinker_action
from models.el_farol import MODEL_NAME as EFMODEL_NAME
from models.el_farol import set_env_attrs as ef_set_env_attrs
from models.fashion import set_up as faset_up
from models.fashion import follower_action, common_action, tsetter_action
from models.fashion import MODEL_NAME as FAMODEL_NAME
from models.fmarket import market_maker_action, trend_follower_action
from models.fmarket import set_up as fmset_up
from models.fmarket import value_investor_action
from models.fmarket import MODEL_NAME as FMMODEL_NAME
from models.fmarket import set_env_attrs as fm_set_env_attrs
from models.forestfire import set_up as ffset_up
from models.forestfire import tree_action
from models.forestfire import MODEL_NAME as FFMODEL_NAME
from models.forestfire import set_env_attrs as ff_set_env_attrs
from models.sandpile import set_up as sandset_up
from models.sandpile import sandpile_action
from models.sandpile import MODEL_NAME as SAMODEL_NAME
from models.sandpile import set_env_attrs as sa_set_env_attrs
from models.segregation import set_up as segset_up
from models.segregation import seg_agent_action
from models.segregation import MODEL_NAME as SEMODEL_NAME
from models.wolfsheep import set_up as wsset_up
from models.wolfsheep import sheep_action, wolf_action
from models.wolfsheep import create_sheep, create_wolf
from models.wolfsheep import MODEL_NAME as WOMODEL_NAME
from epidemics.epidemic import set_up as epset_up
from epidemics.epidemic import people_action
from epidemics.epidemic import set_env_attrs as ep_set_env_attrs
from epidemics.epidemic import MODEL_NAME as EPMODEL_NAME
from capital.money import set_up as mnset_up
from capital.money import money_trader_action
from capital.money import MODEL_NAME as MOMODEL_NAME
from capital.money import set_env_attrs as mn_set_env_attrs
from capital.complementary import set_up as cpset_up
from capital.complementary import MODEL_NAME as CPMODEL_NAME
from capital.complementary import set_env_attrs as cp_set_env_attrs
from capital.complementary import MODEL_NAME as CMMODEL_NAME
from capital.trade_utils import seek_a_trade_w_comp


env_attrs = {
    COMODEL_NAME: co_set_env_attrs,
    CPMODEL_NAME: cp_set_env_attrs,
    EFMODEL_NAME: ef_set_env_attrs,
    EPMODEL_NAME: ep_set_env_attrs,
    FFMODEL_NAME: ff_set_env_attrs,
    FMMODEL_NAME: fm_set_env_attrs,
    MOMODEL_NAME: mn_set_env_attrs,
    SAMODEL_NAME: sa_set_env_attrs,
}

setup_dict = {
    BAMODEL_NAME: bactset_up,
    BSMODEL_NAME: baset_up,
    CMMODEL_NAME: cpset_up,
    COMODEL_NAME: coset_up,
    EFMODEL_NAME: efset_up,
    EPMODEL_NAME: epset_up,
    FAMODEL_NAME: faset_up,
    FMMODEL_NAME: fmset_up,
    FFMODEL_NAME: ffset_up,
    MOMODEL_NAME: mnset_up,
    SAMODEL_NAME: sandset_up,
    SEMODEL_NAME: segset_up,
    WOMODEL_NAME: wsset_up,
}

action_dict = {
    "agent_action": agent_action,
    "babysitter_action": babysitter_action,
    "bacterium_action": bacterium_action,
    "central_bank_action": central_bank_action,
    "common_action": common_action,
    "coop_action": coop_action,
    "drinker_action": drinker_action,
    "follower_action": follower_action,
    "market_maker_action": market_maker_action,
    "nutrient_action": nutrient_action,
    "sheep_action": sheep_action,
    "wolf_action": wolf_action,
    "toxin_action": toxin_action,
    "sandpile_action": sandpile_action,
    "seg_agent_action": seg_agent_action,
    "tsetter_action": tsetter_action,
    "tree_action": tree_action,
    "people_action": people_action,
    "trend_follower_action": trend_follower_action,
    "value_investor_action": value_investor_action,
    "money_trader_action": money_trader_action,
    "seek_a_trade_w_comp": seek_a_trade_w_comp,
}


member_creator_dict = {
    "create_sheep": create_sheep,
    "create_wolf": create_wolf,
}
