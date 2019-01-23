"""
This file defines Place, which is a collection
of entities that share a place.
"""
from composite import Composite


class SpatialRelation():
    def __init__(self, distance, theta):
        self.distance = distance
        self.theta = theta


class Place(Composite):
    """
    A collection of entities that share a location.
    The location is related to others by a distance
    and an angle.
    A set of places is essentially a (distance) weighted
    graph, but one with a built-in geometrical representation,
    due to theta.
    """

    def __init__(self, name, attrs=None, members=None):
        super().__init__(name, attrs=attrs, members=members)
