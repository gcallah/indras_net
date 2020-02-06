import json
import sys
from pydoc import locate
from unittest import TestCase, skip

from indra.registry import get_env


class TestAllModels(TestCase):
    def setUp(self):
        self.models = {}
        with open("models.json") as json_file:
            data = json.load(json_file)
            for mdl_json in data["models_database"]:
                model = locate("models." + mdl_json["run"])
                model.set_up()
                self.models[mdl_json["name"]] = get_env()

    def tearDown(self):
        self.models = []

    @skip("Must rewrite this test in light of new env handling.")
    def test_models(self):
        for name, env in self.models.items():
            print("Testing " + name + "...", file=sys.stderr)
            self.assertTrue(env.runN(2) > 0)
