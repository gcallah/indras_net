"""
Setup an interesting interactive env in which to do play.
"""

from test_entity import *
from test_composite import *
from itime import *

newton = create_newton()
leibniz = create_leibniz()
hardy = create_hardy()
ramanujan = create_ramanujan()
littlewood = create_littlewood()
ramsey = create_ramsey()
calc = create_calcguys()
camb = create_cambguys()
maths = create_mathguys()
math_hist = Time("Hist", periods=8)
