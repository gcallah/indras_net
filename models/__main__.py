import json

import models.fashion
import models.forestfire
import models.sandpile
import models.wolfsheep


def main(args=None):
    with open("models.json", 'r') as f:
        models = json.load(f)
    print(json.dumps(models, indent=4))


if __name__ == "__main__":
    main()
