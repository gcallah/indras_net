#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:55:22 2019

@author: selina
"""
import random
from numpy import random as np_random

MIN_CAR_LIFE = .2

dealer_num = int(input("Enter the number of dealers: "))
round_num = int(input("Enter the number of cars each dealer prepared: "))
result_dic = {}
for i in range(dealer_num):
    center_score = np_random.uniform(1, 5)
    lst = [max(round(random.gauss(center_score, 0.7), 1),
               MIN_CAR_LIFE)
           for i in range(round_num)]
    key = "dealer" + str(i)
    result_dic[key] = lst
    print("{ \"", key, "\": {",
          "mean:", round(center_score, 1), ","
          "scores:", result_dic[key],
          "}},")
