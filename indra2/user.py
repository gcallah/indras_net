"""
This file defines User, which represents a user in our system.
"""
# import json

from indra2.agent import Agent  # , DEBUG2  # DEBUG,

TERMINAL = "terminal"
WEB = "web"
GUI = "gui"
NOT_IMPL = "Choice not yet implemented."


def not_impl(user):
    return user.tell(NOT_IMPL)


def run(user):
    try:
        steps = int(user.ask("How many periods?"))
        user.env.runN(periods=steps)
    except (ValueError, TypeError) as e:
        user.tell("You must enter an integer value for # of steps: " + str(e))


def leave(user):
    user.tell("Goodbye, " + user.name + ", I will miss you!")
    exit(0)


def plot(user):
    user.tell("Drawing a plot.")
    user.env.plot()


MSG = 0
FUNC = 1

QUIT = 0
RUN = 1


term_menu = {RUN: (str(RUN) + ") Run for N periods (DEFAULT).", run),
             2: ("2) Display the population graph.", not_impl),
             3: ("3) Display the plot.", plot),
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
        choice = int(self.ask("Type the # of your choice then Enter:",
                     default=RUN))
        if choice in term_menu:
            term_menu[choice][FUNC](self)
        else:
            self.tell("Invalid option.")
