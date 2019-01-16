"""
This file defines Place, which is a collection
of entities that share a place. A boolean flag may make this
a Place exlusive to a single entity.
"""
from entity import def_coords
from composite import Composite


class Place(Composite):
    """
    A collection of entities that share a location.
    The 'atomic' param to the constructor will indicate
    whether only one entity can occupy this place.
    We will make atomic=False the default, since it
    is the atomic=True case that will require over-riding
    many of the Composite class's methods.
    """

    def __init__(self, name, attrs=None, members=None,
                 coords=def_coords, atomic=False):
        super().__init__(name, attrs=attrs, members=members)
        self.coords = coords
