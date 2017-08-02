import sys

import bigbox.__main__
import models.__main__
import schelling.__main__

MODULE_NAME = 0
MODULE_MAIN = 1

modules = {1: ("Big Box", bigbox.__main__.main),
           2: ("General models", models.__main__.main),
           3: ("Schelling models", schelling.__main__.main)
           }

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("The modules containing models are: ")
    for num, module in modules.items():
        print(str(num) + ". " + module[MODULE_NAME])
    choice = int(
                input("Enter module number to view avialable models: "))
    modules[choice][MODULE_MAIN]()

if __name__ == "__main__":
    main()
