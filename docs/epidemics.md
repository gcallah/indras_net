# Agent-Based Modeling for Epidemics

What we are up to.

Parameters:
- social distancing
- immune period

Research on default parameters and realistic modeling:  
Current Starting Parameters (build f52a5b3)
- Grid Height: 20
- Grid Width: 20
- Mean Period of Immunity: 10
- Population Density: 0.44
- Death Rate: 0.06
- Duration of infectious period: 2
- Rate of Infection if exposed: 0.5
- Social Distancing distance: 2
- Max move distance: 3
- Ratio initially infected: 0.02
- Distance disease can be transmitted: 1
- What percent of people wear masks: 0.5

R0 averages to around 1 after 40 periods. Currently the simulation ends
with on average, near entire population death given enough time. 
However this is mostly due to very small amount of lingering cases that
continue to spread to very few people.

Base values: Figure 1

Modifying period of immunity:
- Increased to 15 (+5): Insignificant slow of spread.
- Increased to 20 (+10): Insignificant slow of spread, however larger
 immune population.
- Increased to 40 (+30): Significant slowdown of spread. Around 1.25x.
- Increased to 80 (+70): Slowdown of around 2x. Significant increase in 
immune population
- Decreased to 5 (-5): Significant increase in deaths. 1.3x higher.

Modifying death rate:
-Decreased to 0.04 (-0.02): Slightly more healthy people, slightly less dead.
-Decreased to 0.02 (-0.04): Significantly more healthy people., and less 
than half the normal dead.
-Increased to 0.08 (+0.02): Deaths overtake healthy population.
-Increased to 0.12 (+0.06): Deaths have nearly doubled.
-Increased to 0.20 (+0.14): Deaths doubled.

Modifying population density:


Modifying Duration of infectious period:
-Decreased to 1 (-1): NO significant change.
-Increased to 3 (+1):
-Increased to 5 (+3): Slightly more deaths.
-Increased to 10 (+8): Despite number of contagious jumping up, no
significant changes to overall healthy or dead populatin.
