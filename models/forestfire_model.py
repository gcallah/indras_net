import random

import indra.spatial_agent as sa
import indra.grid_env as grid


X = 0
Y = 1


class Tree(sa.SpatialAgent):
    '''
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    '''
    def __init__(self, x, y):
        '''
        Create a new tree.
        Args:
            x, y: The tree's coordinates on the grid.
        '''
        name = "Tree at %i %i" % (x, y)
        super().__init__(name, "burn")
        self.pos = (x, y)

    def change_type(self, new_type):
        """
        This is intended simply to turn Trees into
        BurningTrees or DeadTrees. Since those classes
        have no code and just make graphing work
        right, this should be safe!
        """
        old_type = type(self)
        self.__class__ = new_type
        self.env.change_agent_type(self, old_type, new_type)

    def act(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        if type(self) == BurningTree:
            for neighbor in self.env.neighbor_iter(self.pos[X], self.pos[Y]):
                if type(neighbor) == Tree:
                    neighbor.change_type(BurningTree)
            self.change_type(DeadTree)

    def get_pos(self):
        return self.pos


class BurningTree(Tree):
    """
    No code needed. It just changes the type for AgentPop
    """


class DeadTree(Tree):
    """
    No code needed. It just changes the type for AgentPop
    """


class ForestFire(grid.GridEnv):
    '''
    Simple Forest Fire model.
    '''
    def __init__(self, height, width, density, model_nm="ForestFire"):
        '''
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        super().__init__("Forest Fire", height, width, model_nm)
        self.density = density
        self.burning_type = "BurningTree"

        # Place a tree in each cell with Prob = density
        for cell in self.coord_iter():
            x = cell[1]
            y = cell[2]
            if random.random() < self.density:
                # Create a tree
                if x == 0:
                    # all trees in col 0 start on fire
                    new_tree = BurningTree(x, y)
                else:
                    new_tree = Tree(x, y)
                self.position_agent(new_tree, x, y)
        self.running = True

    def step(self):
        super().step()
        # Halt if no more fire
        if self.get_pop(self.burning_type) == 0:
            return "The fire is out!"
