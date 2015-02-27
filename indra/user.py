"""
user.py
Manages the user for the Indra system.
"""

import indra.entity as ent


class User(ent.Entity):
    """
    We will represent the user to the system as another entity.
    """

    # user types
    TERMINAL = "terminal"
    IPYTHON = "iPython"
    IPYTHON_NB = "iPython Notebook"

    def __init__(self, nm, utype):
        super().__init__(nm)
        self.utype = utype

    def tell(self, msg):
        """
        Screen the details of output from models.
        """
        if self.utype in [User.TERMINAL, User.IPYTHON,
                          User.IPYTHON_NB]:
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
        if(self.utype in [User.TERMINAL, User.IPYTHON,
                          User.IPYTHON_NB]):
            return input(msg)
