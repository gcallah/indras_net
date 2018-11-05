# import indra.vector_space as vs
# import indra.vs_agent as va
import indra.grid_env as grid

import random


class Route:
    def __init__(self, name):
        self.intersections = []
        self.count = 0
        self.name = name
        self.heavy_p = 100
        self.light_p = 100
        return

    def travelRoute(self):
        self.count = self.count + 1
        for intersection in self.intersections:
            # move
            # intersection.travelIntersection()
            pass
        return

    def getCount(self):
        return self.count


class RouteWork:

    def __init__(self):
        self.roads = []
        return

    def add(self, name):
        newRoad = Road(name)
        self.roads.append(newRoad)


class Slow:
    def __init__(self):
        self.name = "slow"
        self.available = []
        return

    def travel(self):
        for route in self.availableRoutes:
            move = random.random()
            if move <= Road.slow_p:
                route.travelRoute()
        return

    def addRoute(self, route):
        self.available.append(route)
        return


class Fast:
    def __init__(self):
        self.name = "FAST"
        self.avaiable = []
        return

    def travel(self):
        for route in self.avaiable:
            travel = random.random()
            if travel <= Road.fast_p:
                route.travelRoute()
        return

    def addRoute(self, route):
        self.avaiable.append(route)


class Intersection:
    def __init__(self, name):
        self.neighbours = []
        self.name = name
        self.count = 0
        return

    def intersaction(self):
        self.count += 1

    def getCount(self):
        return self.count

    def addNeighbour(self, node):
        self.neighbours.append(node)
        return


class Graph:
    intersectionArr = []

    def __init__(self):
        self.intersectionArr = []
        return

    def addRelation(self, intersection1, intersection2):
        intersection1.add(intersection2)
        return

    def addTwoRelation(self, inter1, inter2):
        self.addRelation(inter1, inter2)
        self.addRelation(inter2, inter1)
        return


class Road:
    fast_p = 100
    slow_p = 0


class SimInteractiveEnv(grid.GridEnv):
    def __init__(self, name, width, height, torus=False,
                 model_nm='sim_interactive', props=None):
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, props=props)
        self.plot_title = name
