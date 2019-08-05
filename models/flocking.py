"""
    This is the flocking model written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.env import Env
from indra.display_methods import BLUE, TREE

MODEL_NAME = "flocking"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BIRDS = 10
DEF_DESIRED_DISTANCE = 2
BIRD_MAX_MOVE = 2

flock = None
the_sky = None


def calc_angle(agent1, agent2):
    pos1 = agent1.get_pos()
    print("Pos1 = ", pos1)
    return atan(pos1)  # you must calculate!


def bird_action(this_bird):
    nearest_bird = this_bird.locator.get_closest_agent(this_bird)
    if nearest_bird is not None:
        curr_distance = distance(this_bird, nearest_bird)
        print("Distance between ", nearest_bird, " and ", this_bird,
              " is ", curr_distance)
        angle_to_nearest = calc_angle(this_bird, nearest_bird)
        if curr_distance < DEF_DESIRED_DISTANCE:
            this_bird["angle"] = (angle_to_nearest + 180) % 360
        else:
            this_bird["angle"] = angle_to_nearest
    return False


def create_bird(name, i):
    """
    Creates a bird with a numbered name and an action function
    making it flock.
    """
    return Agent(name + str(i), action=bird_action,
                 attrs={"max_move": BIRD_MAX_MOVE,
                        "angle": 0})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)

    flock = Composite("Birds", {"color": BLUE, "marker": TREE},
                      member_creator=create_bird,
                      num_members=pa.get('num_flock', DEF_NUM_BIRDS))

    the_sky = Env("the_sky",
                  height=pa.get('grid_height', DEF_HEIGHT),
                  width=pa.get('grid_width', DEF_WIDTH),
                  members=[flock])
    return (the_sky, flock)


def main():
    global flock
    global the_sky

    (the_sky, flock) = set_up()
    the_sky()
    return 0


if __name__ == "__main__":
    main()
