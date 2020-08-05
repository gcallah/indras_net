# Agent-Based Modeling for Epidemics

What we are up to.

Parameters:
- social distancing
- immune period

Research on default parameters and realistic modeling:  
Current Starting Parameters (build e979d94)
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

Modifying period of immunity:
- Increased to 15 (+5): Insignificant slow of spread.
- Increased to 20 (+10): Insignificant slow of spread.
- Increased to 40 (+30): Significant slowdown of spread. Around 2x.
