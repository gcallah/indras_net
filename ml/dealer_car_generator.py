#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:55:22 2019

@author: selina
"""
import random
from numpy import random as np_random
dealer_num = int(input("Enter the number of dealers: "))
round_num = int(input("Enter the number of cars each dealer prepared: "))
result_dic = {}
for i in range(dealer_num):
    center_score = np_random.uniform(1, 5)
    lst = [abs(round(random.gauss(center_score, 0.7), 1))
           for i in range(round_num)]
    result_dic["dealer" + str(i)] = lst
print(result_dic)
