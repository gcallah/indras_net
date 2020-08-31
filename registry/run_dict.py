"""
The file to register functions we need to restore at run time.

What we need in here for a new online model:

- the model's name
- all action functions -- reg them in `action_dict`
- the model's `set_up()` function -- reg it in `setup_dict`
- the model's `set_env_attrs()` function, IF it exists
  (not every model needs one -- only to restore special functions to the
  env)
  reg it in `env_attrs`

"""
from models.bacteria import bacterium_action, toxin_action, nutrient_action
from models.bacteria import set_up as ba_set_up
from models.bacteria import MODEL_NAME as BA_MODEL_NAME
from models.basic import agent_action
from models.basic import set_up as bs_set_up
from models.basic import MODEL_NAME as BS_MODEL_NAME
from models.coop import babysitter_action, coop_action, central_bank_action
from models.coop import set_up as co_set_up
from models.coop import MODEL_NAME as CO_MODEL_NAME
from models.coop import set_env_attrs as co_set_env_attrs
from models.el_farol import set_up as ef_set_up
from models.el_farol import drinker_action
from models.el_farol import MODEL_NAME as EF_MODEL_NAME
from models.el_farol import set_env_attrs as ef_set_env_attrs
from models.fashion import set_up as fa_set_up
from models.fashion import follower_action, common_action, tsetter_action
from models.fashion import MODEL_NAME as FA_MODEL_NAME
from models.fmarket import market_maker_action, trend_follower_action
from models.fmarket import set_up as fm_set_up
from models.fmarket import value_investor_action
from models.fmarket import MODEL_NAME as FM_MODEL_NAME
from models.fmarket import set_env_attrs as fm_set_env_attrs
from models.forestfire import set_up as ff_set_up
from models.forestfire import tree_action
from models.forestfire import MODEL_NAME as FF_MODEL_NAME
from models.forestfire import set_env_attrs as ff_set_env_attrs
from models.gameoflife import set_up as gl_set_up
from models.gameoflife import gameoflife_action as gl_action
from models.gameoflife import MODEL_NAME as GL_MODEL_NAME
from models.sandpile import set_up as sa_set_up
from models.sandpile import sandpile_action
from models.sandpile import MODEL_NAME as SA_MODEL_NAME
from models.sandpile import set_env_attrs as sa_set_env_attrs
from models.segregation import set_up as se_set_up
from models.segregation import seg_agent_action
from models.segregation import MODEL_NAME as SE_MODEL_NAME
from models.wolfram import set_up as wf_set_up
from models.wolfram import wolfram_action as wf_action
from models.wolfram import MODEL_NAME as WF_MODEL_NAME
from models.wolfsheep import set_up as ws_set_up
from models.wolfsheep import sheep_action, wolf_action
from models.wolfsheep import create_sheep, create_wolf
from models.wolfsheep import MODEL_NAME as WO_MODEL_NAME
from epidemics.epidemic import set_up as ep_set_up
from epidemics.epidemic import person_action
from epidemics.epidemic import set_env_attrs as ep_set_env_attrs
from epidemics.epidemic import MODEL_NAME as EP_MODEL_NAME
from capital.money import set_up as mn_set_up
from capital.money import money_trader_action
from capital.money import MODEL_NAME as MO_MODEL_NAME
from capital.money import set_env_attrs as mn_set_env_attrs
from capital.complementary import set_up as cp_set_up
from capital.complementary import MODEL_NAME as CP_MODEL_NAME
from capital.complementary import set_env_attrs as cp_set_env_attrs
from capital.complementary import MODEL_NAME as CM_MODEL_NAME
from capital.trade_utils import seek_a_trade_w_comp


env_attrs = {
    CO_MODEL_NAME: co_set_env_attrs,
    CP_MODEL_NAME: cp_set_env_attrs,
    EF_MODEL_NAME: ef_set_env_attrs,
    EP_MODEL_NAME: ep_set_env_attrs,
    FF_MODEL_NAME: ff_set_env_attrs,
    FM_MODEL_NAME: fm_set_env_attrs,
    MO_MODEL_NAME: mn_set_env_attrs,
    SA_MODEL_NAME: sa_set_env_attrs,
}

setup_dict = {
    BA_MODEL_NAME: ba_set_up,
    BS_MODEL_NAME: bs_set_up,
    CM_MODEL_NAME: cp_set_up,
    CO_MODEL_NAME: co_set_up,
    EF_MODEL_NAME: ef_set_up,
    EP_MODEL_NAME: ep_set_up,
    FA_MODEL_NAME: fa_set_up,
    FM_MODEL_NAME: fm_set_up,
    FF_MODEL_NAME: ff_set_up,
    GL_MODEL_NAME: gl_set_up,
    MO_MODEL_NAME: mn_set_up,
    SA_MODEL_NAME: sa_set_up,
    SE_MODEL_NAME: se_set_up,
    WO_MODEL_NAME: ws_set_up,
    WF_MODEL_NAME: wf_set_up,
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
    "gameoflife_action": gl_action,
    "market_maker_action": market_maker_action,
    "nutrient_action": nutrient_action,
    "sheep_action": sheep_action,
    "wolf_action": wolf_action,
    "wolfram_action": wf_action,
    "toxin_action": toxin_action,
    "sandpile_action": sandpile_action,
    "seg_agent_action": seg_agent_action,
    "tsetter_action": tsetter_action,
    "tree_action": tree_action,
    "person_action": person_action,
    "trend_follower_action": trend_follower_action,
    "value_investor_action": value_investor_action,
    "money_trader_action": money_trader_action,
    "seek_a_trade_w_comp": seek_a_trade_w_comp,
}


member_creator_dict = {
    "create_sheep": create_sheep,
    "create_wolf": create_wolf,
}
