"""
grid_agent.py
Overrides get_pos for SpatialAgent.
Maybe other things for grid as well.
"""

# import logging
import indra.spatial_agent as sa


class GridAgent(sa.SpatialAgent):
    """
    This class is the parent of all entities that are
    located in a grid space (and might or might not move in it)
    """

    def __init__(self, name, goal, max_move=0.0, max_detect=0.0):
        super().__init__(name, goal, max_move=0.0, max_detect=0.0)
        self.cell = None

    def get_pos(self):
        """
        Our pos is just x, y
        """
        return self.pos
        # return self.cell.get_pos()

    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!
        """
        safe_fields = super().to_json()
        safe_fields["pos"] = self.pos
        return safe_fields
