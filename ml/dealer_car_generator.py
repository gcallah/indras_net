#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:55:22 2019

@author: selina
"""
import json
import random
from numpy import random as np_random

MIN_CAR_LIFE = .2
POS_EMOJIS = ["smiley", "laughing", "relaxing", "wink"]
NEG_EMOJIS = ["unnatural", "ambiguous", "hesitate", "eye rolling"]
MEAN_SCORE = 3
dealers = {}
dealer_num = int(input("Enter the number of dealers: "))
round_num = int(input("Enter the number of cars each dealer prepared: "))
for i in range(dealer_num):
    center_score = np_random.uniform(1, 5)
    lst = [max(round(random.gauss(center_score, 0.7), 1),
               MIN_CAR_LIFE)
           for i in range(round_num)]
    dealer = {}
    dealer_name = "dealer" + str(i)
    if center_score >= MEAN_SCORE:
        emoji = random.choice(POS_EMOJIS)
    else:
        emoji = random.choice(NEG_EMOJIS)
    dealers[dealer_name] = {
        'emoji': emoji,
        'scores': lst
    }

with open('data.json', 'w') as f:
    json.dump(dealers, f)
