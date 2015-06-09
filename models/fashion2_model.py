"""
wolfsheep_model.py
Wolves and sheep roaming a meadow, with wolves eating sheep
that get near them.
"""
import logging
import indra.grid_env as ge
import indra.grid_agent as ga

fashions = ["blue", "red"]

BLUE = 0
RED = 1
INIT_FLWR = BLUE
INIT_HPST = RED

FSHN_TO_TRACK = BLUE


class Fashionista(ga.GridAgent):
    """
    A creature: moves around randomly.
    Reproduction to be added.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal)
        self.max_move = max_move
        self.fashion = None

    def act(self):
        move_view = self.get_square_view(self.max_move)
        self.env.move_to_empty(self, grid_view=move_view)

    def change_fashion(self):
        """
        Switch my fashion.
        """
        if self.fashion == RED:
            self.fashion = BLUE
        else:
            self.fashion = RED
        # self.env.record_fashion_change(self)
        print(self.name + " is changing fashions")
        logging.info(self.name + " is changing fashions")


class Follower(Fashionista):
    """
    A fashion follower: tries to switch to hipsters' fashions.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.fashion = INIT_FLWR

    def act(self):
        super().act()
        has_my_fashion = 0
        not_my_fashion = 0
        for hipster in filter(lambda a: isinstance(a, Hipster),
                              self.neighbor_iter()):
            if hipster.fashion == self.fashion:
                has_my_fashion += 1
            else:
                not_my_fashion += 1
        if not_my_fashion > has_my_fashion:
            self.change_fashion()


class Hipster(Fashionista):
    """
    A fashion hipster: tries to not look like followers.
    """
    def __init__(self, name, goal, max_move):
        super().__init__(name, goal, max_move)
        self.fashion = INIT_HPST

    def act(self):
        super().act()
        has_my_fashion = 0
        not_my_fashion = 0
        for follower in filter(lambda a: isinstance(a, Follower),
                               self.neighbor_iter()):
            if follower.fashion == self.fashion:
                has_my_fashion += 1
            else:
                not_my_fashion += 1
        if not_my_fashion < has_my_fashion:
            self.change_fashion()


class Society(ge.GridEnv):
    """
    A society of hipsters and followers.
    """
