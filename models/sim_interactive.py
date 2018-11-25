import indra.vector_space as vs
import indra.vs_agent as va
import indra.grid_env as grid

import random
"""
Created on Mon Sep 10 17:30:05 2018
@authors: wenxuan ruan
    yadong Li
"""

X = 0
Y = 1

SLOWSPEED = 1
FASTSPEED = 3

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
            intersection.travelIntersection()
        return

    def getCount(self):
        return self.count


class RouteNetwork:

    routes = []

    def __init__(self):
        self.routes = []
        return

    def add(self, name):
        newRoute = Route(name)
        self.routes.append(newRoute)

# class Slow:
#         newRoad = Road(name)
#         self.roads.append(newRoad)

class Vehicle(va.VSAgent):

    def __init__(self, name):
        super.__init__(name)
        self.name = name

    def travel(self, speed):
        x = self.pos[X]
        y = self.pos[Y]

        if speed == "slow":
            if self.env.is_cell_empty(x + SLOWSPEED, y):
                self.env.move(self, x + SLOWSPEED, Y)
        elif speed == "fast":
            if self.env.is_cell_empty(x + FASTSPEED, y + 1):
                self.env.move(self, x + FASTSPEED, Y)

class Slow(Vehicle):
    def __init__(self, num):
        self.name = "slow"
        self.available = []
        self.num = num

    def travel(self):
        for route in self.available:
            move = random.random()
            if move <= Route.heavy_p:
                route.travelRoute()
                super.travel('slow')

    def addRoute(self, route):
        self.available.append(route)


class Fast(Vehicle):
    def __init__(self, num):
        self.name = "FAST"
        self.avaiable = []
        self.num = num

    def travel(self):
        for route in self.avaiable:
            travel = random.random()
            if travel <= Route.light_p:
                route.travelRoute()
                super.travel('fast')

    def addRoute(self, route):
        self.avaiable.append(route)

class Intersection:

    def __init__(self, name):
        self.neighbours = []
        self.name = name
        self.trafficCount = 0

    def travelIntersection(self):
        self.trafficCount += 1

    def getTrafficCount(self):
        return self.trafficCount

    def addNeighbour(self, newNeighbour):
        self.neighbours.append(newNeighbour)


class SimInteractiveEnv(grid.GridEnv):
    def __init__(self, name, width, height, torus=False,
                 model_nm='sim_interactive', props=None):
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, props=props)
        self.plot_title = name
        self.num_moves = 0
        self.move_hist = []
        self.menu.view.del_menu_item("v")  # no line graph in this model
        self.intersectionArr = []

    def addRelation(self, intersection1, intersection2):
        intersection1.addNeighbour(intersection2)

    def addTwoWayRelation(self, inter1, inter2):
        intersection1 = self.get(inter1)
        intersection2 = self.get(inter2)
        self.addRelation(intersection1, intersection2)
        self.addRelation(intersection2, intersection1)

    def addOneWayRelation(self, inter1, inter2):
        intersection1 = self.get(inter1)
        intersection2 = self.get(inter2)
        self.addRelation(intersection1, intersection2)

    def getIntersection(self, interName):
        if len(self.intersectionArr) == 0:
            self.intersectionArr.append(Intersection(interName))
            return self.intersectionArr[0]

        for intersection in self.intersectionArr:
            if intersection.name == interName:
                return intersection

        self.intersectionArr.append(Intersection(interName))
        return self.intersectionArr[0]




