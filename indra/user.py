"""
user.py
Manages the user for the Indra system.
"""

# import logging
from clint.textui import colored, puts, indent
import indra.entity as ent

# user types
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"

MENU = "menu"
PROMPT = "prompt"
ERROR = "error"
INFO = "info"

text_colors = {MENU: colored.blue,
               PROMPT: colored.magenta,
               ERROR: colored.red,
               INFO: colored.black}


def ask(msg):
    puts(text_colors[PROMPT](msg), newline=False)
    return input()


def tell(msg, type=INFO, indnt=0):
    if indnt <= 0:
        puts(text_colors[type](msg))
    else:
        with indent(indnt):
            puts(text_colors[type](msg))


class User(ent.Entity):
    """
    We will represent the user to the system as another entity.
    """

    def __init__(self, nm, utype=TERMINAL):
        super().__init__(nm)
        self.utype = utype

    def tell(self, msg, type=INFO, indnt=0):
        """
        Screen the details of output from models.
        """
        if msg and self.utype in [TERMINAL, IPYTHON, IPYTHON_NB]:
            return tell(msg, type=type, indnt=indnt)

    def ask_for_ltr(self, msg):
        """
        Screen the details of input from models.
        """
        choice = self.ask(msg)
        return choice.strip()

    def ask(self, msg):
        """
        Screen the details of input from models.
        """
        assert self.utype in [TERMINAL, IPYTHON, IPYTHON_NB]
        if(self.utype in [TERMINAL, IPYTHON, IPYTHON_NB]):
            return ask(msg)
