import json

import models.fashion
import models.forestfire
import models.sandpile
import models.wolfsheep


def main(args=None):
    models = None
    models_db = None
    with open("models.json", 'r') as f:
        models_db = json.load(f)
    models = models_db["models_database"]
    print("Welcome to Indra! Please choose a model:")
    for choice, model in enumerate(models):
        print(choice, ". ", model["name"])
    while True:
        choice = int(input())
        if choice > 0 and choice < len(models):
            print(models[choice]["run"])

if __name__ == "__main__":
    main()
