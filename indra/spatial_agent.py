"""
Filename: spatial_agent.py
Author: Gene Callahan
"""

# import logging
import indra.entity as ent

MAX_EXCLUDE = 10

class SpatialAgent(ent.Agent):
    """
    This class is the parent of all entities that are
    located in space (and might or might not move in it)
    """

    def __init__(self, name, goal, max_move=0, max_detect=1):
        super().__init__(name, goal)
        self.max_move = max_move
        self.max_detect = max_detect
        self.__pos = None

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["max_move"] = self.max_move
        safe_fields["max_detect"] = self.max_detect
        safe_fields["pos"] = self.pos
        return safe_fields

    def from_json_preadd(self, json_input):
        super().from_json_preadd(json_input)

        self.pos = json_input["pos"]

