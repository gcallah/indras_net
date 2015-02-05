# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 16:45:50 2014

@author: Gene and Brandon
"""
import height_agent
num_agents = 10


env = height_agent.HeightEnv()


for i in range(num_agents):
    env.add_agent(height_agent.HeightAgent('george' + str(i), i+1))

env.run()

