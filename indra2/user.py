"""
This file defines Time, which is a collection
of agents that share a timeline.
"""
# import json

from indra2.agent import Agent, DEBUG2  # DEBUG,

TERMINAL = "terminal"
WEB = "web"
GUI = "gui"


def not_impl(user):
    user.tell("Choice not yet implemented.")


def run(user):
    steps = int(user.ask("How many periods?"))
    user.env.runN(periods=steps)


def leave(user):
    user.tell("Goodbye, faithless user!")
    exit(0)
    
def scatter_plot(user, env):
    user.tell("Drawing the scatter plot!")
    env.plot()

MSG = 0
FUNC = 1


term_menu = {1: ("1) Run for N periods.", run),
             2: ("2) Display the population graph.", not_impl),
             3: ("3) Display the scatter plot.", scatter_plot),
             4: ("4) Leave menu for interactive python session.", not_impl),
             0: ("0) Quit.", leave)}


class TermUser(Agent):
    """
    A representation of the user in the system.
    """

    def __init__(self, name, env, **kwargs):
        super().__init__(name, **kwargs)
        self.env = env  # this class needs this all the time, we think

    def tell(self, msg, end='\n'):
        print(msg, end=end)

    def ask(self, msg):
        self.tell(msg, end=' ')
        return input()

    def __call__(self):
        self.tell("What would you like to do?")
        for key, item in term_menu.items():
            self.tell(item[MSG])
        choice = int(self.ask("Type the # of your choice then Enter:"))
        if DEBUG2:
            print(choice)
        if choice in term_menu:
            # If the choice is to draw a scatter plot
            if choice == 3: 
                term_menu[choice][FUNC](self, self.env)
            # Other cases
            else: 
                term_menu[choice][FUNC](self)
        else:
            self.tell("Invalid option.")
