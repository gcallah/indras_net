import random

class Route:
    count = 0
    name = "not set"
    fast_p = 100
    slow_p = 100
    intersections = []
    
    def __init__(self, name):
        self.intersections = []
        self.count = 0
        self.name = name
        self.heavy_p = 100
        self.light_p = 100
        return
        
    def travelRoute(self):
        self.count = self.count + 1
        for intersection in intersections:
            # move
            # intersection.travelIntersection()
        return
    
    def getCount(self):
        return count

class RouteWork:
    roads = []
    def __init__(self):
        self.roads = []
        return 

    def add(self, name):
        newRoad = Road(name)  
        roads.append(newRoad)

class Slow:
    name = "DEFAULT"
    avaiable = []

    def __init__(self):
        self.name = "slow"
        self.avaiable = []
        return
    
    def travel(self):
        for route in self.availableRoutes:
            move = random.random()
            if move <= road.slow_p:
                route.travelRoute()
        return

class Fast:
    name = "DEFAULT"
    avaiable = []

def __init__(self):
    self.name = "FAST"
    self.avaiable = []
    return

def travel(self):
    for route in self.avaiable:
        travel = random.random()
        if travel <= road.fast_p:
            route.travelRoute()
    return

def addRoute(self, route):
    avaiable.append(route)
    return