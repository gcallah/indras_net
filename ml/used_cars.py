from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from registry.registry import get_env, get_prop
from indra.utils import init_props
from ml.dealer_factory import generate_dealer
from ml.buyer_action_s import create_buyer_s as selina_cb
from ml.buyer_action_a import create_buyer_a as ava_cb


MODEL_NAME = "used_cars"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_DEALER = 500
DEF_NUM_BUYER = 10

AVA_BUYER_GRP = "Ava_buyer_group"
SELINA_BUYER_GRP = "Selina_buyer_group"
DEALER_GRP = "Dealer_group"

'''
Goal:
    1. see emojis (from Prof); then see rating factor
    2. Multi regression line for ML
    3. contest period - new set of dealers following the
    same rules;
'''


def set_up(props=None):  # testcase???
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props, model_dir="ml")
    group = []
    group.append(Composite(DEALER_GRP, {"color": BLUE},
                           member_creator=generate_dealer,
                           num_members=get_prop('num_dealers',
                                                DEF_NUM_DEALER)))
# can we put the testing period in to composite too?
    group.append(Composite(AVA_BUYER_GRP, {"color": RED},
                           member_creator=ava_cb,
                           num_members=get_prop('num_buyers', DEF_NUM_BUYER)))

    group.append(Composite(SELINA_BUYER_GRP, {"color": RED},
                           member_creator=selina_cb,
                           num_members=get_prop('num_buyers', DEF_NUM_BUYER)))

    Env(MODEL_NAME,
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=group)


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
