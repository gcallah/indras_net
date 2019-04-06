# created based on C. Warrick's page here:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scrip    ts/

import sys
import os

MODEL_NAME = 0
MODEL_RUN = 1


def entry_point(args, models):
    print("In this module, the models available to run are: ")
    for num, model in models.items():
        print(str(num) + ". " + model[MODEL_NAME])
    choice = int(input("Enter model number to run it: "))
    models[choice][MODEL_RUN]()
