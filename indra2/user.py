"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json

from indra2.agent import Agent  # , DEBUG2  # DEBUG,

TERMINAL = "terminal"
WEB = "web"
GUI = "gui"


def not_impl(user):
    user.tell("Choice not yet implemented.")


def run(user):
    try:
        steps = int(user.ask("How many periods?"))
        user.env.runN(periods=steps)
    except (ValueError, TypeError) as e:
        user.tell("You must enter an integer value for # of steps: " + str(e))


def leave(user):
    user.tell("Goodbye, " + user.name + ", I will miss you!")
    exit(0)


def scatter_plot(user):
    user.tell("Drawing a scatter plot.")
    user.env.plot()


MSG = 0
FUNC = 1

QUIT = 0
RUN = 1


term_menu = {RUN: (str(RUN) + ") Run for N periods (DEFAULT).", run),
             2: ("2) Display the population graph.", not_impl),
             3: ("3) Display the scatter plot.", scatter_plot),
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
        except ValueError:
            self.tell("Invalid option.")
