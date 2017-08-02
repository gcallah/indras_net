# created based on C. Warrick's page here:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

import bigbox.big_box_run

MODEL_NAME = 0
MODEL_RUN = 1

models = {1: ("Big Box", bigbox.big_box_run.run)}


def main(args=None):
    print("In this module, the models available to run are: ")
    for num, model in models.items():
        print(str(num) + ". " + model[MODEL_NAME])
    choice = int(input("Enter model number to run it: "))
    models[choice][MODEL_RUN]()

if __name__ == "__main__":
    main()
