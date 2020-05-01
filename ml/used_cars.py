from indra.composite import Composite
from indra.display_methods import RED, BLUE
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from registry.registry import get_env, get_prop
from indra.utils import init_props
from ml.dealer_factory import generate_dealer
from ml.buyer_action_s import create_buyer

MODEL_NAME = "used_cars"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_DEALER = 500
DEF_NUM_BUYER = 10

BUYER_GRP = "Buyer_group"
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
    init_props(MODEL_NAME, props)
    group = []
    group.append(Composite(DEALER_GRP, {"color": BLUE},
                           member_creator=generate_dealer(),
                           num_members=get_prop('num_dealers',
                                                DEF_NUM_DEALER)))
# can we put the testing period in to composite too?
    group.append(Composite(BUYER_GRP, {"color": RED},
                           member_creator=create_buyer,
                           num_members=get_prop('num_buyers', DEF_NUM_BUYER)))

    Env("Car market",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=group)


def main():
    set_up()
    get_env()()
    return 0


if __name__ == "__main__":
    main()
