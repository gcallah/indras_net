"""
This file defines User, which represents a user in our system.
"""
import os
import json
from indra.agent import Agent  # , DEBUG2  # DEBUG,
from IPython import embed

TERMINAL = "terminal"
TEST = "test"
API = "api"
GUI = "gui"
NOT_IMPL = "Choice not yet implemented."
CANT_ASK_TEST = "Can't ask anything of a scripted test"
DEF_STEPS = 1
USER_EXIT = -999

menu_dir = os.getenv("INDRA_HOME", ".") + "/indra"
menu_file = "menu.json"
menu_src = menu_dir + "/" + menu_file


def not_impl(user):
    return user.tell(NOT_IMPL)


def run(user, test_run=False):
    steps = 0
    acts = 0
    try:
        if not test_run:
            steps = user.ask("How many periods?")
            if steps is None or steps == "" or steps.isspace():
                steps = DEF_STEPS
            else:
                steps = int(steps)
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
    return USER_EXIT


def scatter_plot(user):
    user.tell("Drawing a scatter plot.")
    return user.env.scatter_graph()


def line_graph(user):
    user.tell("Drawing a line graph.")
    return user.env.line_graph()


def ipython(user):
    embed()
    return 0


menu_functions = {
    "run": run,
    "leave": leave,
    "scatter_plot": scatter_plot,
    "line_graph": line_graph,
    "ipython": ipython,
}


def get_menu_json():
    menu_json = None
    with open(menu_src, 'r') as f:
        menu_db = json.load(f)
        menu_json = menu_db["menu_database"]
    return menu_json


class User(Agent):
    """
    A representation of the user in the system.
    """
    def __init__(self, name, env, **kwargs):
        super().__init__(name, **kwargs)
        self.env = env  # this class needs this all the time, we think


class TermUser(User):
    """
    A representation of the user on a terminal.
    """
    def __init__(self, name, env, **kwargs):
        super().__init__(name, env, **kwargs)

    def tell(self, msg, end='\n'):
        """
        How to tell the user something.
        """
        print(msg, end=end)
        return msg

    def ask(self, msg, default=None):
        """
        How to ask the user something.
        """
        self.tell(msg, end=' ')
        choice = input()
        if not choice:
            return default
        else:
            return choice

    def log(self, msg, end='\n'):
        """
        How to log something for this type of user.
        Our default is going to be the same as tell, for now!
        """
        return self.user.tell(msg, end)

    def __call__(self):
        DEFAULT_CHOICE = '0'
        menu = get_menu_json()
        menu_title = "Displaying the menu"
        stars = "*" * len(menu_title)
        self.tell("What would you like to do?")
        print("\n",
              stars, "\n",
              menu_title, "\n",
              stars)
        for choice, menu_item in enumerate(menu):
            print(str(choice) + ". ", menu_item["question"])
        c = input()
        if not c or c.isspace():
            c = DEFAULT_CHOICE
        choice = int(c)
        if choice >= 0 and choice < len(menu):
            return menu_functions[menu[choice]["func"]](self)
        else:
            self.user.tell("Invalid Option")


class TestUser(TermUser):
    """
        This is our test user, who has some characteristics different from the
        terminal user, such as overriding ask() and __call__().
    """
    def ask(self, msg, default=None):
        """
            Can't ask anything of a scripted test!
        """
        return self.tell(CANT_ASK_TEST, end=' ')

    def __call__(self):
        """
            Can't present menu to a scripted test!
        """
        run(self)  # noqa: W391


class APIUser(TermUser):
    """
    This is our web user, who is expected to communicate with a web page
    frontend.
    """
    def tell(self, msg, end='\n'):
        """
        Tell the user something by showing it on the web page
        The below code is just a possible way to implement this!
        """
        return {"msg_to_user": '"' + msg + '"'}

    def ask(self, msg, default=None):
        """
        Ask the user something and present it to the web page
        """
        # Some json thing
        pass

    def __call__(self):
        return get_menu_json()
