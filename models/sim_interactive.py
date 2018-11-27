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

SLOW_AGENT = "Slow"
FAST_AGENT = "FAST"


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


class Vehicle(va.VSAgent):

    def __init__(self, name, acceleration, deceleration):
        super().__init__(name, acceleration, deceleration)
        self.name = name
        self.speed = 0.1 + random.uniform(0, 0.9)
        self.acceleration = acceleration
        self.deceleration = deceleration

    def accelerate(self):
        self.speed += self.acceleration

    def decelerate(self, targetSpeed):
        self.speed = targetSpeed - self.deceleration

    def travel(self, grid_env):
        x = self.pos[X]
        # If there is a car ahead
        if grid_env[x+1]:
            self.decelerate(grid_env[x+1].speed)
        else:
            self.accelerate()

        if self.speed < grid_env.minSpeed:
            self.speed = grid_env.minSpeed
        if self.speed > grid_env.maxSpeed:
            self.speed = grid_env.maxSpeed

    def to_json(self):
        safe_fields = super().to_json()
        return safe_fields




class Slow(Vehicle):
    def __init__(self, name, acceleration, deceleration):
        super().__init__(name, acceleration, deceleration)
        self.speed = 0.1 + random.uniform(0, 0.5)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["color"] = "Red"
        return safe_fields


class Fast(Vehicle):
    def __init__(self, name, acceleration, deceleration):
        super().__init__(name, acceleration, deceleration)
        self.speed = 0.1 + random.uniform(0.5, 1)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["color"] = "Blue"
        return safe_fields

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
    def __init__(self, name, width, height, 
                 model_nm=None, props=None):
        # print("About to call GridEnv init.")
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, props=props)
        self.plot_title = name
        self.num_moves = 0
        self.move_hist = []
        self.menu.view.del_menu_item("v")  # no line graph in this model
        self.intersectionArr = []

    def set_agent_color(self):
        self.set_var_color(SLOW_AGENT, 'r')
        self.set_var_color(FAST_AGENT, 'b')

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




