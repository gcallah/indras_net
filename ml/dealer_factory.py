#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 22:55:22 2019

@author: selina, ava and prof. c
"""
# import os
# import json
import random
from indra.agent import Agent


MAX_DEALERS = 99999999
TEST_DEALERS = 6
NUM_DEALS = 4

CORR_SCALAR = 3
MIN_CAR_LIFE = .2
MEAN_CAR_LIFE = 5.0
MAX_CAR_LIFE = 10
CAR_LIFE_SIGMA = 2
DEF_CORRELATIONS = {
                   "smiley": .4,
                   "laughing": .2,
                   "relaxed": .8,
                   "wink": .1,
                   "well-dressed": .3,
                   "unnatural": -.7,
                   "ambiguous": 0,
                   "hesitant": -.4,
                   "dirty-showroom": -.1,
                   "eye-rolling": -.8}

emoji_list = list(DEF_CORRELATIONS.keys())


def dealer_action(agent, **kwargs):
    return False


def constrain_car_life(unconstrained):
    return max(MIN_CAR_LIFE, min(MAX_CAR_LIFE, unconstrained))


def get_emojis(dealer):
    return dealer.attrs["emojis"]


def sell_car(dealer):
    car_life = random.gauss(dealer.attrs["avg_car_life"], CAR_LIFE_SIGMA)
    return constrain_car_life(car_life)


def avg_life_from_emojis(emojis):
    this_car_life = MEAN_CAR_LIFE
    for emoji in emojis:
        this_car_life += DEF_CORRELATIONS[emoji] * CORR_SCALAR
    return constrain_car_life(round(this_car_life, 2))


def generate_dealer(unused1, unused2, *kwargs):
    dealer = Agent("dealer" + str(random.randint(0, MAX_DEALERS)),
                   action=dealer_action)
    num_emojis = random.randint(1, len(DEF_CORRELATIONS) // 2)
    dealer.attrs["emojis"] = random.sample(emoji_list, num_emojis)
    dealer.attrs["avg_car_life"] = avg_life_from_emojis(dealer.attrs["emojis"])
    return dealer


def main():
    dealers = []
    print("Generating dealers:")
    for i in range(TEST_DEALERS):
        dealers.append(generate_dealer())
        print(repr(dealers[i]))
    print("\n**********\nGetting cars:")
    for dealer in dealers:
        print("Dealer emojis = ", get_emojis(dealer))
        for j in range(NUM_DEALS):
            car_life = sell_car(dealer)
            print("For dealer with car life", dealer.attrs["avg_car_life"],
                  "we get a car with", car_life, "lifespan")


if __name__ == "__main__":
    main()
