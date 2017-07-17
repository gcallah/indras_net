"""
user.py
Manages the user for the Indra system.
"""

# import logging
# we are going to do some shenanigans so we can use clint if present
#  and work around if not
MENU = "menu"
PROMPT = "prompt"
ERROR = "error"
INFO = "info"
text_colors = None
clint_present = True
try:
    from clint.textui import colored, puts, indent
    text_colors = {MENU: colored.blue,
                   PROMPT: colored.magenta,
                   ERROR: colored.red,
                   INFO: colored.black}
except ImportError:
    clint_present = False
    text_colors = {MENU: None,
                   PROMPT: None,
                   ERROR: None,
                   INFO: None}

import indra.entity as ent

# user types
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"


def ask(msg):
    if clint_present:
        puts(text_colors[PROMPT](msg), newline=False)
    else:
        print(msg, end='')
    return input()

def tell(msg, type=INFO, indnt=0):
    if indnt <= 0:
        if clint_present:
            puts(text_colors[type](msg))
        else:
            print(msg)
    else:
        if clint_present:
            with indent(indnt):
                puts(text_colors[type](msg))
        else:
            for i in range(0, indnt):
                msg = '  ' + msg
            print(msg)

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
