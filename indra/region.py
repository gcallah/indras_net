
# these go in space.py:

class Region:
    # constructor, contains(), and the coords data member

class CompositeRegion(Region):
    # a list or set of regions
    # set operations to add and delete members?


# this will be the test code, in tests/test_space.py:

def test_contains(self):
    test_reg = Region(((0,0), (3,0), (0,3), (3,3)
    assertTrue(test_reg.contains(0,0))
    assertFalse(test_reg.contains(3,3))

def test_composite_contains(self):
    # build a couple of regions, build a composite
    # from them, and test as above
