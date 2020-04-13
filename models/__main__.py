import json

from registry.run_dict import rdict


def main(args=None):
    welcome = "Welcome to Indra! Please choose a model:"
    stars = "*" * len(welcome)
    model_db = None
    model_list = None
    with open("models.json", 'r') as f:
        model_db = json.load(f)
    model_list = model_db["models_database"]
    while True:
        print("\n",
              stars, "\n",
              welcome, "\n",
              stars)
        for choice, model in enumerate(model_list):
            print(str(choice) + ". ", model["name"])
        choice = int(input())
        if 0 <= choice < len(model_list):
            rdict[model_list[choice]["run"]]()
        else:
            return 0


if __name__ == "__main__":
    main()
