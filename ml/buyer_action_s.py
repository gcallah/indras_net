#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 10:22:19 2020

@author: selina
"""

'''
Goal:
    1. training period:
    - make a list of good dealer and bad dealer
    - buy from anyone;
    - add dealer ratings to attribute
    - agent try to multilinear regression
    2. see emojis (from Prof); then see rating factor
    3. Multi regression line for ML
    4. Bank and sugeron examples doing machine learning
    on training - then on test set.
    5. contest period - new set of dealers following the
    same rules;
'''
import random
#import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
sns.set()

from indra.agent import Agent
from registry.registry import get_group, get_env
from ml.dealer_factory import generate_dealer
#from ml.stradegy import * 


DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BUYER  = 10
DEF_NUM_SELLER = 10

MIN_CAR_LIFE = .2
MEDIUM_CAR_LIFE = 5
MAX_CAR_LIFE = 10

MATURE_BOUND = 100


BUYER_GRP = "Buyer_group"
DEALER_GRP = "Dealer_group"
strategies = {}
# should put in jupiter notebook
def multi_linear_regression(agent):
    data = pd.DataFrame(agent["purchase_hist"])
    y = data["car_life"] 
    emojis = list(agent["emoji_experienced"].keys())
    x1 = data[emojis]
    x=sm.add_constant(x1)
    results=sm.OLS(y,x).fit()
    results.summary()
    print(results.params)
    
# different strategies
strategies = {"s1": {"func": multi_linear_regression} }
    
def is_dealer(agent):  # testcase need changes
    return get_group(DEALER_GRP).ismember(agent)

def get_car_life(dealer):  # testcase done
    """
    Display dealer's information and car
    for debug purpose
    """
    print("Getting car from dealer", dealer)
    return dealer["avg_car_life"]

def is_mature(buyer):  # testcase done
    """
    check if buyer has enough experience
    to make its own decision
    """
    return buyer["maturity"] > MATURE_BOUND

def learning_w_strategy(agent, dealer):
    organize_data(agent)
    print("Investigating, buyer strategy =", agent["strategy"])
    agent["strategy"]["func"](agent)
    agent["learnt"] = True
    # may need to self-testing stage too 
    
def buy_w_experience(agent, dealer):
    pass

def organize_data(agent):
    '''Supervised learnig data collection and organization period'''
    organized_purchase_hist = []
    title_row = ["car_life"]
    for emoji in agent["emoji_experienced"]:
        title_row.append(emoji)
    organized_purchase_hist.append(title_row)
    for purchase in agent["purchase_hist"]:
        curr_purchase = [0]*len(agent["emoji_experienced"])
        curr_purchase[0] = purchase["car_life"]
        for emoji in purchase["emojis"]:
            curr_purchase[agent["emoji_experienced"][emoji]] = 1
        # the purchase history should look like y x1 x2 x3...
        organized_purchase_hist.append(curr_purchase)
        print(curr_purchase)
    agent["purchase_hist"] = organized_purchase_hist


def buy_from_dealer(agent, dealer):
    ''' used for immature buyers. 
    Supervised learnig data collection period'''
    agent["has_car"] = True
    print("I am an immature buyer. I got a car that last ", 
          str(dealer["avg_car_life"]),
          ", and my dealer's emoji(s) is/are: ",
          str(dealer["emojis"]))
    curr_purchase = {"car_life" : dealer["avg_car_life"],
                     "emojis" : dealer["emojis"]}
    for emoji in dealer["emojis"]:
        if emoji in agent["emoji_experienced"]:
            agent["emoji_experienced"][emoji] = len(agent["emoji_experienced"]) + 1 
            # skip the 0 
    agent["purchase_hist"].append(curr_purchase)
    agent["car_life"] = dealer["avg_car_life"]

def buyer_action(agent):  # how to write this testcase
    """
    This functions lets buyer
    to decides whether wants to buy a car or not
    """
    print("_" * 20)
    print("Agent: " + agent.name)
    agent["maturity"] += 1
    if not agent["has_car"]:
        my_dealer = get_env().get_neighbor_of_groupX(agent,
                                                     get_group(DEALER_GRP),
                                                     hood_size=4)
        if my_dealer is None:
            print("No dealers nearby.")
        elif not is_mature(agent):
            buy_from_dealer(agent, my_dealer)        
        else:
            if(not agent["learnt"]):
                learning_w_strategy(agent, my_dealer)
            buy_w_experience(agent, my_dealer)
            
    else:
        # return False means to move
        print("I have a car!")
        agent["car_life"] -= 1
        if agent["car_life"] <= 0:
            agent["has_car"] = False 
    return False



def create_dealer(name, i, props=None):  # testcase done
    """
    Create a dealer agent.
    """
    return generate_dealer()

def create_buyer(name, i, props=None):  # testcase done
    """
    Create a buyer agent.
    """
    return Agent(name + str(i),
                 action=buyer_action,
                 attrs={"has_car": False,
                        "maturity": 0,
                        "purchase_hist": [],  # list of purchased correlation
                        "emoji_experienced": {},  # emojis encountered during immature period
                        "learnt": False,
                        "strategy": random.choice(list(strategies.keys())),
                        "car_life": 0
                        })


