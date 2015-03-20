"""
user.py
Manages the user for the Indra system.
"""

# import logging
import indra.entity as ent

# user types
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"


class User(ent.Entity):
    """
    We will represent the user to the system as another entity.
    """

    def __init__(self, nm, utype=TERMINAL):
        super().__init__(nm)
        self.utype = utype

    def tell(self, msg):
        """
        Screen the details of output from models.
        """
        assert self.utype in [TERMINAL, IPYTHON, IPYTHON_NB]
        if self.utype in [TERMINAL, IPYTHON, IPYTHON_NB]:
            print(msg)

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
            return input(msg)
