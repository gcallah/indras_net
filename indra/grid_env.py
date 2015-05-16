"""
grid_env.py

This is an adaptation of the:

Mesa Space Module
=================================

From the GMU Mesa project.

Objects used to add a spatial component to a model.

GridEnv: base grid, a simple list-of-lists.

MultiGridEnv: extension to Grid where each cell is a set of objects.

"""

# Instruction for PyLint to suppress variable name errors,
# since we have a
# good reason to use one-character variable names for x and y.
# pylint: disable=invalid-name

import random
import itertools
import logging
import indra.node as node
import indra.spatial_env as se

RANDOM = -1

X = 0
Y = 1


class Cell(node.Node):
    """
    Cells hold the grid contents.
    They also have a record of where they are in the grid.
    """
    def __init__(self, coords, contents=None):
        super().__init__(None)
        self.__contents = None
        self.coords = coords
        self.contents = contents

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self, item):
        old_item = self.__contents
        self.__contents = item
        if item is not None:
            item.cell = self
        if old_item is not None:
            old_item.cell = None

    def is_empty(self):
        """
        Return True if cell empty, else False.
        """
        return not self.contents

        """
        Return the coordinates of this cell.
        """
        return self.coords

    def add_item(self, new_item):
        """
        Add new_item to cell contents.
        Every cell item must have a cell
        field to store its location.
        """
        self.contents = new_item

    def remove_item(self, item):
        """
        If item is our object, set contents to None.
        If that is not our object, do nothing.
        """
        if item == self.contents:
            self.contents = None


class GridEnv(se.SpatialEnv):
    """
    Base class for a rectangular grid.

    If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether
            to treat the grid as a torus.

        grid: Internal list-of-lists which holds
            the grid cells themselves.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
        get_neighborhood: Returns the coords surrounding a given cell.
        get_cell_items: Returns the contents of a list of cells
            ((x,y) tuples)
    """

    def __init__(self, name, height, width, torus=False,
                 model_nm=None, preact=False, postact=False):
        """
        Create a new grid.

        Args:
            height, width: The height and width of the grid
            torus: Boolean whether the grid wraps or not.
        """
        super().__init__(name, width, height, preact, postact, model_nm)

        self.torus = torus

        self.grid = []
        self.empties = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell((x, y))
                row.append(cell)
                self.empties.append(cell)
            self.grid.append(row)

    def __iter__(self):
        # create an iterator that chains the
        #  rows of grid together as if one list:
        return itertools.chain(*self.grid)

    def __getitem__(self, index):
        return self.grid[index]

    def add_agent(self, agent, position=True):
        """
        Add an agent and link to cell if present in agent.
        """
        super().add_agent(agent, position)
        if agent.cell is not None:
            if agent.cell.contents is not agent:
                agent.cell.add_item(agent)

    def neighbor_iter(self, x, y, moore=True, torus=False):
        """
        Iterate over our neighbors.
        """
        neighbors = self.get_neighbors(x, y, moore=moore)
        return iter(neighbors)

    def torus_adj(self, coord, dim_len):
        """
        Convert coordinate, handling torus looping.
        """
        if self.torus:
            coord %= dim_len
        return coord

    def out_of_bounds(self, x, y):
        """
        Is point x, y off the grid?
        """
        return(x < 0 or x >= self.width
               or y < 0 or y >= self.height)

    def get_neighborhood(self, x, y, moore,
                         include_center=False, radius=1):
        """
        Return a list of cells that are in the
        neighborhood of a certain point.

        Args:
            x, y: Coordinates for the neighborhood to get.
            moore: If True, return Moore neighborhood
                        (including diagonals)
                   If False, return Von Neumann neighborhood
                        (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of coordinate tuples representing the neighborhood;
                With radius 1, at most 9 if
                Moore, 5 if Von Neumann
                (8 and 4 if not including the center).
        """
        coordinates = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0 and not include_center:
                    continue
                if not moore:
                    # Skip diagonals in Von Neumann neighborhood.
                    if dy != 0 and dx != 0:
                        continue

                px = self.torus_adj(x + dx, self.width)
                py = self.torus_adj(y + dy, self.height)

                # Skip if new coords out of bounds.
                if(self.out_of_bounds(px, py)):
                    continue

                coordinates.append((px, py))
        return coordinates

    def get_neighbors(self, x, y, moore,
                      include_center=False, radius=1):
        """
        Return a list of neighbors to a certain point.

        Args:
            x, y: Coordinates for the neighborhood to get.
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).
        """
        neighborhood = self.get_neighborhood(x, y, moore,
                                             include_center,
                                             radius)
        return self.get_cell_items(neighborhood)

    def get_cell_items(self, cell_list):
        """
        Args:
            cell_list: Array-like of (x, y) tuples

        Returns:
            A list of the contents of the cells identified in cell_list
        """
        items = []
        for x, y in cell_list:
            self._add_members(items, x, y)
        return items

    def exists_empty_cells(self):
        """
        Return True if any cells empty else False.
        """
        return len(self.empties) > 0

    def move_to_empty(self, agent):
        """
        Moves agent to an empty cell, vacating agent's old cell.
        """
        empty_cell = self.find_empty()
        if empty_cell is None:
            logging.ERROR("Agent could not move because no cells are empty")
        else:
            self._move_item(agent, empty_cell)

    def find_empty(self):
        if self.exists_empty_cells():
            cell = random.choice(self.empties)
            return cell
        else:
            return None

    def position_item(self, item, x=RANDOM, y=RANDOM):
        """
        Position an agent on the grid.
        This is used when first placing agents! Use 'move_to_empty()'
        when you want agents to jump to an empty cell.
        If x or y are positive, they are used, but if RANDOM,
        we get a random position.
        Ensure this random position is not occupied (in Grid).
        """
        if x == RANDOM or y == RANDOM:
            cell = self.find_empty()
            if cell is None:
                logging.error("Grid full; %s not added." % (item.name))
                return
        else:
            cell = self._get_cell(x, y)
        self._place_item(cell, item)

    def _place_item(self, cell, item):
        """
        Place an agent in the grid.
        """
        cell.add_item(item)
        if cell in self.empties:
            self.empties.remove(cell)

    def _get_contents(self, x, y):
        """
        Extract contents from cell at x, y
        """
        return self._get_cell(x, y).contents

    def move(self, item, x, y):
        """
        Move item from its old cell to cell at x, y.
        """
        dest = self._get_cell(x, y)
        self._move_item(item, dest)

    def _move_item(self, item, dest):
        old_cell = item.cell
        if old_cell is not None:
            old_cell.remove_item(item)
            self._check_empty(old_cell)
        self._place_item(dest, item)

    def _check_empty(self, cell):
        if cell.is_empty():
            self.empties.append(cell)

    def _add_members(self, target_list, x, y):
        """
        Helper method to append the contents of a cell
            to the given list.
        Override for other grid types.
        """
        items = self._get_contents(x, y)
        if items is not None:
            target_list.append(items)

    def _get_cell(self, x, y):
        return self.grid[y][x]

    def is_cell_empty(self, x, y):
        """
        Returns True if cell is empty, else False.
        A non-existent cell is NOT empty, i.e., not free
        to move to!
        """
        if self.out_of_bounds(x, y):
            return False
        else:
            return self._get_contents(x, y) is None


class MultiGridEnv(GridEnv):
    """
    Grid where each cell can contain more than one object.

    Grid cells are indexed by [y][x], where [0][0] is assumed to be the top-left
    and [height-1][width-1] is the bottom-right. If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other.

    Each grid cell holds a set object.

    Properties:
        width, height: The grid's width and height.

        torus: Boolean which determines whether
            to treat the grid as a torus.

        grid: Internal list-of-lists which holds
            the grid cells themselves.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
    """

    def _add_members(self, target_list, x, y):
        """
        Helper method to add all objects in the
            given cell to the target_list.
        """
        for a in self.grid[y][x]:
            target_list.append(a)
