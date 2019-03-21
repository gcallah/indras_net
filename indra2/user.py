"""
This file defines User, which represents a user in our system.
"""
# import json

from indra2.agent import Agent  # , DEBUG2  # DEBUG,

TERMINAL = "terminal"
TEST = "test"
WEB = "web"
GUI = "gui"
NOT_IMPL = "Choice not yet implemented."

DEF_STEPS = 10


def not_impl(user):
    return user.tell(NOT_IMPL)


def run(user, test_run=False):
    steps = 0
    acts = 0
    try:
        if not test_run:
            steps = int(user.ask("How many periods?"))
            user.tell("Steps = " + str(steps))
        else:
            steps = DEF_STEPS
        acts = user.env.runN(periods=steps)
    except (ValueError, TypeError) as e:
        user.tell("You must enter an integer value for # of steps: "
                  + str(e))
    return acts


def leave(user):
    user.tell("Goodbye, " + user.name + ", I will miss you!")
    exit(0)


def scatter_plot(user):
    user.tell("Drawing a scatter plot.")
    return user.env.scatter_graph()


def line_graph(user):
    user.tell("Drawing a line graph.")
    ret = user.env.line_graph()
    return ret


MSG = 0
FUNC = 1

QUIT = 0
RUN = 1


term_menu = {RUN: (str(RUN) + ") Run for N periods (DEFAULT).", run),
             2: ("2) Display a population graph.", line_graph),
             3: ("3) Display a scatter plot.", scatter_plot),
             4: ("4) Leave menu for interactive python session.", not_impl),
             QUIT: (str(QUIT) + ") Quit.", leave)}


class TermUser(Agent):
    """
    A representation of the user in the system.
    """

    def __init__(self, name, env, **kwargs):
        super().__init__(name, **kwargs)
        self.env = env  # this class needs this all the time, we think

    def tell(self, msg, end='\n'):
        print(msg, end=end)
        return msg

    def ask(self, msg, default=None):
        self.tell(msg, end=' ')
        choice = input()
        if not choice:
            return default
        else:
            return choice

    def __call__(self):
        self.tell("What would you like to do?")
        for key, item in term_menu.items():
            self.tell(item[MSG])
        try:
            choice = int(self.ask("Type the # of your choice then Enter:",
                         default=RUN))
            if choice in term_menu:
                term_menu[choice][FUNC](self)
            else:
                raise ValueError
        except ValueError as e:
            self.tell("Invalid option: " + str(e))


class TestUser(TermUser):
    """
        Should just override ask() and __call__()
        from TermUser.
    """
    def ask(self, msg, default=None):
        """
            Can't ask anything of a scripted test!
        """
        pass

    def __call__(self):
        """
            Can't present menu to a scripted test!
        """
        pass
