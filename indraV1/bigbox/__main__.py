# created based on C. Warrick's page here:
# https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

from indra.entry_point import entry_point
import bigbox.big_box_run

models = {1: ("Big Box", bigbox.big_box_run.run)}


def main(args=None):
    entry_point(args, models)

if __name__ == "__main__":
    main()
