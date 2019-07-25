import sys
from unittest import TestCase, main
from pydoc import locate

import json


class TestAllModels(TestCase):
    def setUp(self):
        self.models = {}
        with open ("models.json") as json_file:
            data = json.load(json_file)
            for mdl_json in data["models_database"]:
                model = locate("models." + mdl_json["run"])
                env_tup = model.set_up()
                # env is 0th element of tuple:
                self.models[mdl_json["name"]] = env_tup[0]

    def tearDown(self):
        self.models = []

    def test_models(self):
        for name, env in self.models.items():
            print("Testing " + name + "...", file=sys.stderr)
            self.assertTrue(env.runN() > 0)
