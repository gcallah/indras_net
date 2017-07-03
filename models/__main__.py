# created based on C. Warrick's page here:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

import sys
import os

models = {
            "Fashion": "fashion_run.py",
            "Fire": "forestfire_run.py",
            "Sand": "sand_run.py",
            "Wolf Sheep": "wolfsheep_run.py"
         }


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    print("In this module, the models available to run are: ")
    for model_nm in models.keys():
        print(model_nm)
    choice = input("Enter model name to run it: ")

    try:
        os.system("./" + models[choice])
    except Exception:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
