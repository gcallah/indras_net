"""
interactive.py:
Setup an interesting interactive env in which to play
and try out new features.
This just uses agent, composite, and itime.
We're going to do "bad" import *s here because this isn't "real"
code, just a playground for experimenting.
"""

from tests.test_agent import *
from tests.test_composite import *
from itime import *

DEF_WIDTH = 10
DEF_HEIGHT = 10

newton = create_newton()
leibniz = create_leibniz()
hardy = create_hardy()
ramanujan = create_ramanujan()
littlewood = create_littlewood()
ramsey = create_ramsey()
calc = newton + leibniz
camb = create_cambguys()
alt_camb = newton + hardy
maths = create_mathguys()
gauss = Agent("Gauss")
euler = Agent("Euler")
laplace = Agent("Laplace")
germans = Composite("Germans",
                    members={gauss.name: gauss,
                             euler.name: euler})
maths += germans
math_hist = Time("History", members={maths.name: maths})
