# created based on C. Warrick's page here:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scrip    ts/

import sys
import os

MODEL_NAME = 0
MODEL_SCRIPT = 1


def entry_point(args, models):
    if args is None:
        args = sys.argv[1:]

    print("In this module, the models available to run are: ")
    for num, model in models.items():
        print(num + ". " + model[MODEL_NAME])
    choice = input("Enter model number to run it: ")

    try:
        os.system("./" + models[choice][MODEL_SCRIPT])
    except Exception:
        print("Invalid choice.")
