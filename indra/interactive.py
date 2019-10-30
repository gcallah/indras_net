"""
interactive.py:
Setup an interesting interactive env in which to play
and try out new features.
This just uses agent, composite, and itime.
We're going to do "bad" import *s here because this isn't "real"
code, just a playground for experimenting.
"""

from indra.env import *
from indra.tests.test_composite import *

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
germans = Composite("Germans", members=[gauss, euler])

print("Gauss in Germans = ", germans.ismember(str(gauss)))

maths += germans
math_hist = Env("History", members=[maths])
