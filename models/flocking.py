"""
    This is the flocking model written in indra.
"""
import math

from indra.utils import get_props
from indra.agent import Agent, X, Y
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.env import Env
from indra.display_methods import BLUE, TREE
MODEL_NAME = "flocking"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BIRDS = 2
DEF_DESIRED_DISTANCE = 2
BIRD_MAX_MOVE = 2

HALF_CIRCLE = 180
FULL_CIRCLE = 360

flock = None
the_sky = None


def calc_angle(agent1, agent2):
    pos1 = agent1.get_pos()
    print("Coordinates of first point " + str(pos1))
    pos2 = agent2.get_pos()
    print("Coordinates of second point " + str(pos2))
    x = pos2[X] - pos1[X]
    print("Result of x coordinates " + str(x))
    y = pos2[Y] - pos1[Y]
    print("Result of y coordinates " + str(y))
    angle = math.degrees(math.atan2(y, x))
    print("The required angle is " + str(angle))
    angle = angle if angle >= 0 else (angle * -1) + HALF_CIRCLE
    return angle


def bird_action(this_bird):
    nearest_bird = this_bird.locator.get_closest_agent(this_bird)
    if nearest_bird is not None:
        curr_distance = distance(this_bird, nearest_bird)
        print("Distance between ", nearest_bird, " and ", this_bird,
              " is ", curr_distance)
        angle_to_nearest = calc_angle(this_bird, nearest_bird)
        if curr_distance < DEF_DESIRED_DISTANCE:
            this_bird["angle"] = (angle_to_nearest + HALF_CIRCLE) % FULL_CIRCLE
        else:
            this_bird["angle"] = angle_to_nearest
        print(this_bird.name, "'s angle is ", this_bird["angle"])
    return False


def create_bird(name, i, props=None):
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
    pa = get_props(MODEL_NAME, props)

    flock = Composite("Birds", {"color": BLUE, "marker": TREE},
                      member_creator=create_bird,
                      num_members=pa.get('num_birds', DEF_NUM_BIRDS))

    the_sky = Env("the_sky",
                  height=pa.get('grid_height', DEF_HEIGHT),
                  width=pa.get('grid_width', DEF_WIDTH),
                  members=[flock])
    return (the_sky, flock)


def fl_unrestorable(env):
    global flock
    global the_sky
    the_sky = env
    flock = env.registry["Birds"]


def main():
    global flock
    global the_sky

    (the_sky, flock) = set_up()
    the_sky()
    return 0


if __name__ == "__main__":
    main()
