#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:55:22 2019

@author: selina
"""
import os
import json
import random
from numpy import random as np_random
from indra.utils import get_props

MODEL_NAME = "dealer_car_generator"

MIN_CAR_LIFE = .2
POS_EMOJIS = ["smiley", "laughing", "relaxing", "wink"]
NEG_EMOJIS = ["unnatural", "ambiguous", "hesitate", "eye rolling"]
MEAN_SCORE = 3

dealers = {}
pa = get_props(MODEL_NAME, None, model_dir="ml")
dealer_num = pa.get("num_dealers", 10)
car_num = pa.get("num_cars", 50)
for i in range(dealer_num):
    center_score = np_random.uniform(1, 5)
    lst = [max(round(random.gauss(center_score, 0.7), 1),
               MIN_CAR_LIFE)
           for i in range(car_num)]
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
target_dir = os.getcwd() + "/data/"
filename = str(dealer_num) + "dealers_" + str(car_num) + "cars_" + "data.json"
with open(target_dir + filename, 'w') as f:
    json.dump(dealers, f)
